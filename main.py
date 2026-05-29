#!/usr/bin/env python3
"""
Wikipedia Curiosities Scrapper
Scraps the 'Did you know' section from a Wikipedia page and exports to CSV.
"""

import argparse
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

import scrapper

DEFAULT_URL = "https://pt.wikipedia.org/wiki/Wikipédia:Sabia_que"


def validate_url(url: str) -> bool:
    """Validate if the URL has a valid scheme and netloc."""
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def request(url: str) -> BeautifulSoup:
    """Request the HTML page and return a BeautifulSoup object."""
    headers = {"User-Agent": "WikiScrapper/1.0 (Python study project)"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_arguments():
    """Configure and process command line arguments."""
    parser = argparse.ArgumentParser(
        description='Scrap the "Did you know" section from a Wikipedia page',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default PT Wikipedia URL
  python main.py

  # Use a custom URL
  python main.py --url https://en.wikipedia.org/wiki/Wikipedia:Did_you_know

  # Custom output directory and filename
  python main.py --output ./results --name curiosities
        """,
    )

    parser.add_argument(
        "--url",
        type=str,
        default=DEFAULT_URL,
        help=f'Wikipedia "Did you know" page URL (default: PT Wikipedia)',
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data",
        help="Output directory for the CSV file (default: data/)",
    )

    parser.add_argument(
        "--name",
        type=str,
        default="scrap",
        help="CSV filename without extension (default: scrap)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    if not validate_url(args.url):
        print(f"ERROR: Invalid URL: '{args.url}'")
        print("URL must start with http:// or https://")
        return

    print(f"URL: {args.url}")
    print(f"Output: {args.output}/{args.name}.csv")
    print()

    try:
        soup = request(args.url)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect. Check your internet connection.")
        return
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error: {e}")
        return
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed: {e}")
        return

    curiosities = scrapper.curiosity_extract(soup)

    if not curiosities:
        print("WARNING: No curiosities found. The page structure may have changed.")
        return

    try:
        scrapper.scrap_input(
            curiosity=curiosities, data_path=args.output, csv_name=args.name
        )
        print(f"Done. File saved at: {args.output}/{args.name}.csv")
    except Exception as e:
        print(f"ERROR: Could not write CSV: {e}")


if __name__ == "__main__":
    main()