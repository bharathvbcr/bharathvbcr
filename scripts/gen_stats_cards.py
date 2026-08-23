#!/usr/bin/env python3
"""Render the profile stat cards as SVGs from the GitHub API.

Replaces the hosted github-readme-stats widgets, which render an error card
when their deployment runs out of API quota and break entirely when it is
paused. Everything here runs in Actions against the GitHub GraphQL API, so no
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


def collect(user: str, token: str) -> tuple[dict, list[dict], bool]:
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

    ranked = sorted(sizes.items(), key=lambda kv: -kv[1])
    total = sum(sizes.values()) or 1
    languages = [
        {"name": n, "color": colors[n], "pct": size * 100 / total}
        for n, size in ranked
    ]
    return stats, languages, includes_private


def _frame(width: int, height: int, title: str, body: str) -> str:
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" \
xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(title)}">
  <style>
    .title {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {TITLE}; }}
    .label {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {TEXT}; }}
    .value {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {ICON}; }}
    .muted {{ font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: {MUTED}; }}
  </style>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="{RADIUS}" fill="{BG}"/>
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

    stats = languages = None
    used = ""
    includes_private = False
    for index, (var, token) in enumerate(tokens):
        try:
            stats, languages, includes_private = collect(args.user, token)
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
    scope = "public + private" if includes_private else "public only"
    print(f"wrote stats.svg and top-langs.svg to {args.out_dir}")
    print(f"  token: {used} ({scope})")
    print(f"  stats: {stats}")
    print(f"  langs: {[l['name'] for l in languages[:args.langs_count]]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
