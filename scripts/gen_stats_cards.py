#!/usr/bin/env python3
"""Render the profile stat cards as SVGs from the GitHub API.

Replaces the hosted github-readme-stats widgets, which render an error card
when their deployment runs out of API quota and break entirely when it is
paused, and github-readme-activity-graph, whose deployment now answers every
request with HTTP 402 DEPLOYMENT_DISABLED. Everything here runs in Actions against the GitHub GraphQL API, so no
third-party host sees a token and there is no render service to go down: the
profile serves committed SVGs.

Tokens are tried in order: STATS_TOKEN, then GITHUB_TOKEN, then GH_TOKEN. A
PAT in STATS_TOKEN additionally counts private repositories and private
contributions; the built-in GITHUB_TOKEN sees public data only. If STATS_TOKEN
is set but rejected -- expired, revoked, wrong scopes -- the run falls back to
GITHUB_TOKEN and emits a GitHub Actions warning annotation, so an expired PAT
shows up as a visible warning rather than as silently smaller numbers.

Usage:
    STATS_TOKEN=... python3 gen_stats_cards.py --user <login> --out-dir dist
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

API = "https://api.github.com/graphql"

# Highest privilege first. STATS_TOKEN is an optional user PAT that can see
# private repositories; GITHUB_TOKEN is the workflow's built-in public-only token.
TOKEN_VARS = ("STATS_TOKEN", "GITHUB_TOKEN", "GH_TOKEN")

# Matches the profile README's palette.
BG = "#1a0000"
TITLE = "#ff6b6b"
TEXT = "#ffffff"
ICON = "#ff4444"
MUTED = "#ffffff80"
RADIUS = 15

STATS_QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      nodes {
        isPrivate
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


class AuthError(RuntimeError):
    """The token was rejected; a lower-privilege one may still work."""


def _warn(title: str, message: str) -> None:
    """Emit a GitHub Actions warning annotation (plain text off CI)."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::warning title={title}::{message}")
    print(f"WARNING: {title}: {message}", file=sys.stderr)


def candidate_tokens() -> list[tuple[str, str]]:
    """(env var, token) pairs in precedence order, de-duplicated by value."""
    found: list[tuple[str, str]] = []
    seen: set[str] = set()
    for var in TOKEN_VARS:
        value = os.environ.get(var)
        if value and value not in seen:
            seen.add(value)
            found.append((var, value))
    return found


def graphql(query: str, variables: dict, token: str) -> dict:
    request = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-stat-cards",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise AuthError(f"token rejected (HTTP {exc.code})") from exc
        raise
    if "errors" in payload:
        types = {e.get("type") for e in payload["errors"]}
        if types & {"FORBIDDEN", "UNAUTHORIZED"}:
            raise AuthError(f"token rejected: {payload['errors']}")
        raise RuntimeError(f"GraphQL errors: {payload['errors']}")
    return payload["data"]


def collect(user: str, token: str) -> tuple[dict, list[dict], list[dict], bool]:
    data = graphql(STATS_QUERY, {"login": user}, token)["user"]
    repos = data["repositories"]["nodes"]
    contributions = data["contributionsCollection"]

    # Direct evidence rather than inference: if any private repo came back, the
    # token can see private data and these totals include it. restrictedContributions
    # counts private *activity*, which is 0 for plenty of tokens that do see private
    # repos -- using it here reported "public only" for a PAT that clearly wasn't.
    includes_private = any(r["isPrivate"] for r in repos)
    restricted = contributions.get("restrictedContributionsCount") or 0

    stats = {
        "Total Stars": sum(r["stargazerCount"] for r in repos),
        "Total Commits": contributions["totalCommitContributions"] + restricted,
        "Total PRs": data["pullRequests"]["totalCount"],
        "Total Issues": data["issues"]["totalCount"],
        "Contributed to": data["repositories"]["totalCount"],
        "Followers": data["followers"]["totalCount"],
    }

    sizes: dict[str, int] = {}
    colors: dict[str, str] = {}
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            sizes[name] = sizes.get(name, 0) + edge["size"]
            colors[name] = edge["node"]["color"] or "#888888"

    calendar = contributions["contributionCalendar"]
    days = [
        {"date": day["date"], "count": day["contributionCount"]}
        for week in calendar["weeks"]
        for day in week["contributionDays"]
    ]

    ranked = sorted(sizes.items(), key=lambda kv: -kv[1])
    total = sum(sizes.values()) or 1
    languages = [
        {"name": n, "color": colors[n], "pct": size * 100 / total}
        for n, size in ranked
    ]
    return stats, languages, days, includes_private


def _frame(
    width: int,
    height: int,
    title: str,
    body: str,
    defs: str = "",
    extra_style: str = "",
) -> str:
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" \
xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(title)}">
  <style>
    .title {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {TITLE}; }}
    .label {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {TEXT}; }}
    .value {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {ICON}; }}
    .muted {{ font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: {MUTED}; }}
{extra_style}  </style>
{defs}  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="{RADIUS}" fill="{BG}"/>
  <text x="25" y="35" class="title">{escape(title)}</text>
{body}
</svg>
"""


def render_stats(user: str, stats: dict) -> str:
    rows = []
    for i, (label, value) in enumerate(stats.items()):
        y = 70 + i * 26
        rows.append(f'  <text x="25" y="{y}" class="label">{escape(label)}</text>')
        rows.append(f'  <text x="430" y="{y}" class="value" text-anchor="end">{value:,}</text>')
    height = 70 + len(stats) * 26 + 10
    return _frame(495, height, f"{user}'s GitHub Stats", "\n".join(rows))


def render_languages(languages: list[dict], count: int) -> str:
    top = languages[:count]
    width, bar_x, bar_w = 495, 25, 445
    parts, offset = [], 0.0
    shown = sum(lang["pct"] for lang in top) or 1
    for lang in top:
        seg = bar_w * lang["pct"] / shown
        parts.append(
            f'  <rect x="{bar_x + offset:.1f}" y="55" width="{seg:.1f}" height="8" '
            f'fill="{lang["color"]}"/>'
        )
        offset += seg
    for i, lang in enumerate(top):
        col, row = i % 2, i // 2
        x, y = 25 + col * 230, 95 + row * 24
        parts.append(f'  <circle cx="{x + 5}" cy="{y - 4}" r="5" fill="{lang["color"]}"/>')
        parts.append(
            f'  <text x="{x + 18}" y="{y}" class="label">{escape(lang["name"])} '
            f'<tspan class="muted">{lang["pct"]:.1f}%</tspan></text>'
        )
    height = 95 + ((len(top) + 1) // 2) * 24 + 10
    return _frame(width, height, "Most Used Languages", "\n".join(parts))


MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

# Line and fill for the activity graph, carried over from the retired widget's
# query string so the card keeps the palette the README was built around.
LINE = "#ff6b6b"
AREA_TOP = "#8B0000"
AREA_BOTTOM = "#4a0000"
GRID = "#ffffff1a"


def render_activity(user: str, days: list[dict]) -> str:
    """Trend chart of contribution activity over the trailing year.

    Replaces github-readme-activity-graph, whose deployment answers every
    request with HTTP 402 DEPLOYMENT_DISABLED -- the same class of failure that
    already cost this profile its stat cards. The data comes from the calendar
    in the stats query, so this adds no request and leaves no third-party
    render service in the path.

    The series plotted is a trailing 7-day mean, not the raw daily count. Daily
    contributions here are heavy-tailed -- one 141-commit day against a median
    near zero -- and drawn raw the axis is set by that single spike, flattening
    the other 364 days into a line along the bottom. Smoothing shows the shape;
    the axis says which series it is, and the header keeps the two raw numbers
    the average hides.
    """
    width, height = 1000, 300
    left, right, top, bottom = 58, 78, 84, 46
    plot_w, plot_h = width - left - right, height - top - bottom
    base = top + plot_h
    window = 7

    counts = [day["count"] for day in days]
    total = sum(counts)
    busiest = max(counts, default=0)

    trend = [
        sum(counts[max(0, i - window + 1) : i + 1])
        / len(counts[max(0, i - window + 1) : i + 1])
        for i in range(len(counts))
    ]
    peak = max(trend, default=0.0)
    # A contribution-free year would otherwise divide by zero and draw the
    # series straight through the axis labels.
    scale = peak or 1.0
    step = plot_w / (len(days) - 1) if len(days) > 1 else 0.0

    points = [
        (left + i * step, base - (value / scale) * plot_h)
        for i, value in enumerate(trend)
    ]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    area = (
        f"M{points[0][0]:.1f},{base:.1f} "
        + " ".join(f"L{x:.1f},{y:.1f}" for x, y in points)
        + f" L{points[-1][0]:.1f},{base:.1f} Z"
    )

    parts = []
    # Gridlines at 0, half and peak of the plotted series.
    for fraction in (0.0, 0.5, 1.0):
        y = base - fraction * plot_h
        parts.append(
            f'  <line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" '
            f'stroke="{GRID}" stroke-width="1"/>'
        )
        parts.append(
            f'  <text x="{left - 10}" y="{y + 4:.1f}" class="muted" '
            f'text-anchor="end">{peak * fraction:.0f}</text>'
        )

    parts.append(f'  <path d="{area}" fill="url(#activityFill)"/>')
    parts.append(
        f'  <polyline points="{line}" fill="none" stroke="{LINE}" '
        f'stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>'
    )

    # Name the series on the axis it scales. A reader who takes a smoothed
    # curve for daily counts has been misled by the chart, not by the data.
    parts.append(
        f'  <text x="{left - 10}" y="{top - 12}" class="muted" text-anchor="end">'
        f'7-day</text>'
    )
    parts.append(
        f'  <text x="{left}" y="{top - 12}" class="muted">mean contributions '
        f'per day</text>'
    )

    # One month label per boundary, skipped when the previous is still within
    # 46px -- crowded ticks read as noise, not as an axis.
    last_label_x = float("-inf")
    for i, day in enumerate(days):
        if day["date"][8:10] != "01":
            continue
        x = left + i * step
        if x - last_label_x < 46 or x > left + plot_w - 8:
            continue
        parts.append(
            f'  <text x="{x:.1f}" y="{base + 22}" class="muted" '
            f'text-anchor="middle">{MONTHS[int(day["date"][5:7]) - 1]}</text>'
        )
        last_label_x = x

    # The two numbers the mean smooths away, kept where they cannot be misread
    # off the curve.
    parts.append(
        f'  <text x="{width - 25}" y="35" class="peak" text-anchor="end">'
        f'{total:,} contributions</text>'
    )
    parts.append(
        f'  <text x="{width - 25}" y="53" class="muted" text-anchor="end">'
        f'last year &#183; busiest day {busiest}</text>'
    )

    # Current position: the right edge of a trend line is the number a reader
    # is actually looking for, and it is the one point no axis tick lands on.
    end_x, end_y = points[-1]
    parts.append(f'  <circle cx="{end_x:.1f}" cy="{end_y:.1f}" r="3.5" fill="{TEXT}"/>')
    parts.append(
        f'  <text x="{end_x + 9:.1f}" y="{end_y + 4:.1f}" class="peak">'
        f'{trend[-1]:.0f}/day</text>'
    )

    defs = f"""  <defs>
    <linearGradient id="activityFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{AREA_TOP}" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="{AREA_BOTTOM}" stop-opacity="0.05"/>
    </linearGradient>
  </defs>
"""
    extra_style = (
        "    .peak { font: 600 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: "
        + TEXT
        + "; }\n"
    )
    return _frame(
        width,
        height,
        f"{user}'s Contribution Activity",
        "\n".join(parts),
        defs=defs,
        extra_style=extra_style,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("dist"))
    parser.add_argument("--langs-count", type=int, default=6)
    args = parser.parse_args()

    tokens = candidate_tokens()
    if not tokens:
        print(f"one of {', '.join(TOKEN_VARS)} is required", file=sys.stderr)
        return 2

    stats = languages = days = None
    used = ""
    includes_private = False
    for index, (var, token) in enumerate(tokens):
        try:
            stats, languages, days, includes_private = collect(args.user, token)
            used = var
            break
        except AuthError as exc:
            remaining = tokens[index + 1:]
            if not remaining:
                print(f"stat card generation failed: {var} {exc}", file=sys.stderr)
                return 1
            # A silently downgraded card is the failure mode worth surfacing:
            # the numbers would just get smaller with nothing to explain it.
            _warn(
                f"{var} rejected",
                f"{exc}. Falling back to {remaining[0][0]}; private repositories "
                "will not be counted until the token is renewed.",
            )
        except (urllib.error.URLError, RuntimeError, KeyError) as exc:
            # Fail loudly: the workflow keeps the previously committed cards rather
            # than publishing an error card, which is what the hosted widget did.
            print(f"stat card generation failed: {exc}", file=sys.stderr)
            return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "stats.svg").write_text(render_stats(args.user, stats), encoding="utf-8")
    (args.out_dir / "top-langs.svg").write_text(
        render_languages(languages, args.langs_count), encoding="utf-8"
    )
    (args.out_dir / "activity.svg").write_text(
        render_activity(args.user, days), encoding="utf-8"
    )
    scope = "public + private" if includes_private else "public only"
    print(f"wrote stats.svg, top-langs.svg and activity.svg to {args.out_dir}")
    print(f"  token: {used} ({scope})")
    print(f"  stats: {stats}")
    print(f"  langs: {[l['name'] for l in languages[:args.langs_count]]}")
    print(f"  activity: {len(days)} days, {sum(d['count'] for d in days):,} contributions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
