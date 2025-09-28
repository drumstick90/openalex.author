#!/usr/bin/env python3
"""
Planisphere Script: Frequentist coauthor-by-country aggregation for a given OpenAlex author.

Usage:
  python3 planisphere_script.py A41008148            # Author ID
  python3 planisphere_script.py https://openalex.org/A41008148
  python3 planisphere_script.py A41008148 --json     # Print JSON output

Output (text):
  Anchor country (mode of author's affiliations) and top coauthor countries with counts.

Output (JSON with --json):
  {
    "author_id": "A41008148",
    "anchor_iso": "US",
    "co_countries": { "GB": 12, "DE": 7, ... }
  }
"""

import argparse
import json
import sys
import time
from typing import Dict, List, Tuple

import requests

BASE_URL = "https://api.openalex.org"
UA = {'User-Agent': 'Planisphere Script (mailto:your-email@example.com)'}


def normalize_author_id(arg: str) -> str:
    if not arg:
        raise ValueError("Missing author id")
    if "openalex.org/" in arg:
        arg = arg.rstrip("/").split("/")[-1]
    return arg


def fetch_all_works_for_author(author_id: str, per_page: int = 200, max_pages: int = 20, pause_s: float = 0.2) -> List[dict]:
    results: List[dict] = []
    cursor = "*"
    pages = 0
    session = requests.Session()
    session.headers.update(UA)
    while cursor and pages < max_pages:
        url = f"{BASE_URL}/works?filter=author.id:{author_id}&per-page={per_page}&cursor={cursor}"
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        res = data.get("results", [])
        results.extend(res)
        cursor = data.get("meta", {}).get("next_cursor")
        pages += 1
        # be kind
        time.sleep(pause_s)
        if not res:
            break
    return results


def aggregate_countries(author_id: str, works: List[dict]) -> Tuple[str, Dict[str, int]]:
    anchor_countries: Dict[str, int] = {}
    co_countries: Dict[str, int] = {}

    def iso_up(v: str) -> str:
        return (v or "").upper()

    for w in works:
        auths = w.get("authorships", []) or []
        anchor_auth = None
        for a in auths:
            a_id = (((a or {}).get("author", {}) or {}).get("id") or "")
            if a_id.endswith("/" + author_id):
                anchor_auth = a
                break
        if not anchor_auth:
            continue

        anchor_iso_set = set()
        co_iso_set = set()

        for inst in (anchor_auth.get("institutions", []) or []):
            cc = iso_up(inst.get("country_code", ""))
            if cc:
                anchor_iso_set.add(cc)

        for a in auths:
            a_id = (((a or {}).get("author", {}) or {}).get("id") or "")
            if not a_id or a_id.endswith("/" + author_id):
                continue
            for inst in (a.get("institutions", []) or []):
                cc = iso_up(inst.get("country_code", ""))
                if cc:
                    co_iso_set.add(cc)

        if not anchor_iso_set:
            continue
        for cc in anchor_iso_set:
            anchor_countries[cc] = anchor_countries.get(cc, 0) + 1
        for cc in co_iso_set:
            co_countries[cc] = co_countries.get(cc, 0) + 1

    # Mode of anchor countries
    anchor_iso = ""
    mx = -1
    for cc, cnt in anchor_countries.items():
        if cnt > mx:
            mx = cnt
            anchor_iso = cc

    return anchor_iso, co_countries


def main():
    parser = argparse.ArgumentParser(description="Planisphere frequentist coauthor-by-country aggregation")
    parser.add_argument("author", help="OpenAlex author id or URL (e.g., A41008148 or https://openalex.org/A41008148)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = parser.parse_args()

    try:
        author_id = normalize_author_id(args.author)
    except Exception as e:
        print(f"Invalid author: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[+] Fetching works for author {author_id} ...", file=sys.stderr)
    try:
        works = fetch_all_works_for_author(author_id)
    except requests.HTTPError as e:
        print(f"HTTP error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)

    print(f"[+] Processing {len(works)} works...", file=sys.stderr)
    anchor_iso, co_countries = aggregate_countries(author_id, works)

    if args.__dict__["json"]:
        out = {
            "author_id": author_id,
            "anchor_iso": anchor_iso,
            "co_countries": co_countries,
        }
        print(json.dumps(out, indent=2, sort_keys=True))
    else:
        print()
        print("=== Frequentist Coauthor-by-Country ===")
        print(f"Author: {author_id}")
        print(f"Anchor country (mode): {anchor_iso or 'N/A'}")
        print("Top coauthor countries:")
        for cc, cnt in sorted(co_countries.items(), key=lambda x: (-x[1], x[0]))[:50]:
            print(f"  {cc}: {cnt}")


if __name__ == "__main__":
    main()


