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

from gen_stats_cards import render_activity  # noqa: E402

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


if __name__ == "__main__":
    unittest.main()
