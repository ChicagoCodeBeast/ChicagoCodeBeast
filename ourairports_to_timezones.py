#!/usr/bin/env python3
"""
Build an airport code -> timezone CSV from OurAirports data.

The script downloads OurAirports airports.csv, derives IANA timezone from
latitude/longitude, and writes a clean output file.
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
import urllib.request
from typing import Any

try:
    from timezonefinder import TimezoneFinder
except ImportError as exc:  # pragma: no cover - user-facing import hint
    raise SystemExit(
        "Missing dependency: timezonefinder\n"
        "Install it with:\n"
        "  python3 -m pip install timezonefinder\n"
    ) from exc


DEFAULT_URL = "https://ourairports.com/data/airports.csv"
DEFAULT_OUTPUT = "ourairports-airport-timezones.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate airport code + timezone data from OurAirports airports.csv."
        )
    )
    parser.add_argument(
        "--input-url",
        default=DEFAULT_URL,
        help=f"Source CSV URL (default: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional max number of rows to process (useful for quick tests).",
    )
    parser.add_argument(
        "--include-missing-timezone",
        action="store_true",
        help="Include rows even when timezone cannot be derived.",
    )
    parser.add_argument(
        "--include-metadata",
        action="store_true",
        help=(
            "Include extra descriptive columns (name, municipality, country, lat/lon). "
            "Default output includes only iata_code, icao_code, timezone."
        ),
    )
    return parser.parse_args()


def safe_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def download_csv(url: str) -> list[dict[str, Any]]:
    request = urllib.request.Request(url, headers={"User-Agent": "python-urllib/3"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(payload)))


def main() -> int:
    args = parse_args()

    print(f"Downloading {args.input_url} ...")
    try:
        rows = download_csv(args.input_url)
    except Exception as exc:  # pragma: no cover - network-dependent path
        print(f"Failed to download source CSV: {exc}", file=sys.stderr)
        return 1

    tf = TimezoneFinder()
    output_rows: list[dict[str, Any]] = []

    processed = 0
    skipped_no_code = 0
    skipped_no_coords = 0
    skipped_no_timezone = 0

    for row in rows:
        if args.limit is not None and processed >= args.limit:
            break
        processed += 1

        iata = (row.get("iata_code") or "").strip().upper()
        icao = (row.get("icao_code") or "").strip().upper()
        if not iata and not icao:
            skipped_no_code += 1
            continue

        lat = safe_float(row.get("latitude_deg") or "")
        lon = safe_float(row.get("longitude_deg") or "")
        if lat is None or lon is None:
            skipped_no_coords += 1
            continue

        timezone = tf.timezone_at(lat=lat, lng=lon)
        if not timezone and not args.include_missing_timezone:
            skipped_no_timezone += 1
            continue

        output_rows.append(
            {
                "iata_code": iata,
                "icao_code": icao,
                "timezone": timezone or "",
                "name": (row.get("name") or "").strip(),
                "municipality": (row.get("municipality") or "").strip(),
                "iso_country": (row.get("iso_country") or "").strip(),
                "latitude_deg": row.get("latitude_deg") or "",
                "longitude_deg": row.get("longitude_deg") or "",
            }
        )

    if args.include_metadata:
        fieldnames = [
            "iata_code",
            "icao_code",
            "timezone",
            "name",
            "municipality",
            "iso_country",
            "latitude_deg",
            "longitude_deg",
        ]
    else:
        fieldnames = ["iata_code", "icao_code", "timezone"]

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Wrote {len(output_rows)} rows to {args.output}")
    print(f"Processed rows: {processed}")
    print(f"Skipped (no airport code): {skipped_no_code}")
    print(f"Skipped (no coordinates): {skipped_no_coords}")
    print(f"Skipped (no timezone match): {skipped_no_timezone}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
