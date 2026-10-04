#!/usr/bin/env python3
"""Tests for the profile card generator.

Stdlib only, matching the generator: `python3 -m unittest discover scripts`.

These cover the shapes that break a card silently rather than loudly -- a
contribution-free year dividing by zero, a series drawn outside its own
viewBox, an axis labelled with the wrong series. A card that renders but
renders wrong looks exactly like a card that is fine.
"""

from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent))

from gen_stats_cards import (  # noqa: E402
    card_height,
    render_activity,
    render_languages,
    render_stats,
    streaks,
)

SVG_NS = "{http://www.w3.org/2000/svg}"
WIDTH, HEIGHT = 1000, 300


def days_from(counts: list[int], start_month: int = 1) -> list[dict]:
    """Calendar days with real dates, so month-label logic is exercised."""
    out, month, day = [], start_month, 1
    for count in counts:
        out.append({"date": f"2026-{month:02d}-{day:02d}", "count": count})
        day += 1
        if day > 28:
            day, month = 1, month + 1
            if month > 12:
                month = 1
    return out


def coordinates(svg: str) -> list[tuple[float, float]]:
    """Every plotted point in the document, for bounds checking."""
    root = ET.fromstring(svg)
    found: list[tuple[float, float]] = []
    for element in root.iter():
        tag = element.tag.replace(SVG_NS, "")
        if tag == "polyline":
            for pair in element.get("points", "").split():
                x, y = pair.split(",")
                found.append((float(x), float(y)))
        elif tag == "circle":
            found.append((float(element.get("cx")), float(element.get("cy"))))
        elif tag in ("text", "line"):
            if tag == "text":
                found.append((float(element.get("x")), float(element.get("y"))))
            else:
                found.append((float(element.get("x1")), float(element.get("y1"))))
                found.append((float(element.get("x2")), float(element.get("y2"))))
    return found


class ActivityCard(unittest.TestCase):
    def test_renders_well_formed_svg(self):
        svg = render_activity("someone", days_from([1, 4, 9, 2, 0, 7, 3] * 52))
        ET.fromstring(svg)  # raises on malformed output
        self.assertIn('viewBox="0 0 1000 300"', svg)

    def test_contribution_free_year_does_not_divide_by_zero(self):
        # The guard that matters: a flat-zero calendar is a real account state,
        # and an unguarded peak makes the scale 0/0 rather than an empty chart.
        svg = render_activity("someone", days_from([0] * 365))
        ET.fromstring(svg)
        self.assertIn("0 contributions", svg)

    def test_single_day_calendar_renders(self):
        # len(days) - 1 is the x-step divisor; one day makes it zero.
        svg = render_activity("someone", days_from([5]))
        ET.fromstring(svg)

    def test_all_geometry_stays_inside_the_viewbox(self):
        # A spike-dominated year is the case that pushed content off-frame.
        counts = [0] * 300 + [141] + [80] * 64
        for point in coordinates(render_activity("someone", days_from(counts))):
            x, y = point
            self.assertGreaterEqual(x, 0, f"x off-frame at {point}")
            self.assertLessEqual(x, WIDTH, f"x off-frame at {point}")
            self.assertGreaterEqual(y, 0, f"y off-frame at {point}")
            self.assertLessEqual(y, HEIGHT, f"y off-frame at {point}")

    def test_axis_names_the_series_it_scales(self):
        # The plotted series is a 7-day mean. An axis that does not say so
        # invites the curve to be read as daily counts.
        svg = render_activity("someone", days_from([3] * 365))
        self.assertIn("7-day", svg)
        self.assertIn("mean contributions per day", svg)

    def test_header_keeps_the_totals_the_mean_hides(self):
        counts = [0] * 364 + [141]
        svg = render_activity("someone", days_from(counts))
        self.assertIn("141 contributions", svg)  # total
        self.assertIn("busiest day 141", svg)

    def test_smoothing_is_a_trailing_seven_day_mean(self):
        # One contribution on the final day of an otherwise empty year is 1/7
        # of a day averaged over the window, not 1.
        counts = [0] * 364 + [7]
        svg = render_activity("someone", days_from(counts))
        self.assertIn("1/day", svg)

    def test_header_carries_the_streaks(self):
        # The streak used to be a second hosted card; it is read off the same
        # calendar now, so the chart header is where it lives.
        counts = [0] * 300 + [1] * 10 + [0] * 5 + [2] * 50
        svg = render_activity("someone", days_from(counts))
        self.assertIn("50-day streak", svg)
        self.assertIn("longest 50", svg)


class Streaks(unittest.TestCase):
    def test_current_and_longest_runs(self):
        counts = [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1]
        self.assertEqual(streaks(days_from(counts)), (2, 4, False))

    def test_a_quiet_today_does_not_end_the_streak(self):
        # GitHub's calendar includes today. At 9am with nothing pushed yet the
        # run is still alive; only a missed full day ends it.
        counts = [0, 1, 1, 1, 0]
        self.assertEqual(streaks(days_from(counts))[0], 3)

    def test_a_missed_yesterday_does_end_it(self):
        counts = [1, 1, 1, 0, 0]
        self.assertEqual(streaks(days_from(counts))[0], 0)

    def test_a_run_reaching_the_window_start_is_a_lower_bound(self):
        # The calendar is the trailing year. A run that starts at its first day
        # may have started earlier, so the number is a floor, not the streak.
        current, longest, clipped = streaks(days_from([3] * 365))
        self.assertEqual((current, longest, clipped), (365, 365, True))
        svg = render_activity("someone", days_from([3] * 365))
        self.assertIn("365+-day streak", svg)

    def test_empty_calendar(self):
        self.assertEqual(streaks([]), (0, 0, False))
        self.assertEqual(streaks(days_from([0] * 30)), (0, 0, False))


class CardRow(unittest.TestCase):
    """Stats and languages sit side by side in the README at the same width."""

    STATS = {"Total Stars": 24, "Total Commits": 5244, "Total PRs": 12,
             "Total Issues": 2, "Contributed to": 29, "Followers": 4}
    LANGS = [{"name": n, "color": "#888888", "pct": p} for n, p in
             [("Rust", 34.9), ("Swift", 14.2), ("Go", 13.8),
              ("TypeScript", 13.5), ("Python", 8.6), ("Kotlin", 7.5)]]

    @staticmethod
    def size(svg: str) -> tuple[int, int]:
        root = ET.fromstring(svg)
        return int(root.get("width")), int(root.get("height"))

    def test_both_cards_are_the_same_size(self):
        height = card_height(len(self.STATS))
        stats = render_stats("someone", self.STATS, height)
        langs = render_languages(self.LANGS, 6, height)
        self.assertEqual(self.size(stats), self.size(langs))

    def test_language_rows_stay_inside_the_card(self):
        height = card_height(len(self.STATS))
        svg = render_languages(self.LANGS, 6, height)
        for x, y in coordinates(svg):
            self.assertLessEqual(y, height - 12, f"row too low at {(x, y)}")

    def test_more_languages_than_rows_grow_the_card_instead_of_overflowing(self):
        many = self.LANGS * 2
        height = card_height(len(self.STATS))
        svg = render_languages(many, 12, height)
        _, rendered = self.size(svg)
        self.assertGreater(rendered, height)
        for _, y in coordinates(svg):
            self.assertLessEqual(y, rendered - 12)


if __name__ == "__main__":
    unittest.main()
