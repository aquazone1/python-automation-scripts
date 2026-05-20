"""
API Data Fetcher - Fetch, cache, and export data from any REST API
No external dependencies - uses Python standard library only
"""
import json
import csv
import time
import hashlib
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime


CACHE_DIR = Path(".api_cache")


def fetch(
    url: str,
    params: dict = None,
    headers: dict = None,
    method: str = "GET",
    body: dict = None,
    cache_minutes: int = 0,
) -> dict | list | None:
    """
    Fetch data from a REST API endpoint.

    cache_minutes: Cache response for N minutes (0 = no cache).
    Returns parsed JSON response.
    """
    if params:
        url = url + "?" + urllib.parse.urlencode(params)

    if cache_minutes > 0:
        cached = _get_cache(url, cache_minutes)
        if cached is not None:
            print(f"  [CACHE HIT] {url[:80]}")
            return cached

    req_headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if headers:
        req_headers.update(headers)

    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        if cache_minutes > 0:
            _set_cache(url, result)
        return result
    except Exception as e:
        print(f"  API Error: {e}")
        return None


def paginate(
    url: str,
    page_param: str = "page",
    start: int = 1,
    max_pages: int = 10,
    results_key: str = None,
    headers: dict = None,
    delay: float = 0.5,
) -> list:
    """
    Automatically paginate through API results.

    results_key: If the list is nested (e.g., response["data"]), provide the key.
    Stops when an empty page is returned.
    """
    all_items = []
    for page in range(start, start + max_pages):
        print(f"  Fetching page {page}...")
        data = fetch(url, params={page_param: page}, headers=headers)
        if not data:
            break
        items = data[results_key] if results_key and isinstance(data, dict) else data
        if not items:
            print(f"  Empty page at {page}, stopping.")
            break
        all_items.extend(items)
        print(f"    Got {len(items)} items (total: {len(all_items)})")
        time.sleep(delay)
    return all_items


def to_csv(data: list, output_file: str, flatten: bool = True):
    """Export a list of dicts to CSV. Optionally flatten nested objects."""
    if not data:
        print("No data to export.")
        return
    if flatten:
        data = [_flatten(row) for row in data]
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys(), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
    print(f"Exported {len(data)} rows to {output_file}")


def to_json(data, output_file: str):
    Path(output_file).write_text(json.dumps(data, indent=2, ensure_ascii=False))
    count = len(data) if isinstance(data, list) else 1
    print(f"Exported {count} items to {output_file}")


def _flatten(d: dict, parent: str = "", sep: str = "_") -> dict:
    items = {}
    for k, v in d.items():
        key = f"{parent}{sep}{k}" if parent else k
        if isinstance(v, dict):
            items.update(_flatten(v, key, sep))
        else:
            items[key] = v
    return items


def _cache_key(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def _get_cache(url: str, max_age_minutes: int):
    CACHE_DIR.mkdir(exist_ok=True)
    path = CACHE_DIR / f"{_cache_key(url)}.json"
    if not path.exists():
        return None
    age = (time.time() - path.stat().st_mtime) / 60
    if age > max_age_minutes:
        return None
    return json.loads(path.read_text())


def _set_cache(url: str, data):
    CACHE_DIR.mkdir(exist_ok=True)
    path = CACHE_DIR / f"{_cache_key(url)}.json"
    path.write_text(json.dumps(data))


if __name__ == "__main__":
    print("API Data Fetcher - Examples:")
    print()
    print("1. Simple GET request:")
    print("   data = fetch('https://api.example.com/users', headers={'Authorization': 'Bearer TOKEN'})")
    print()
    print("2. With caching (don't refetch for 60 minutes):")
    print("   data = fetch('https://api.example.com/products', cache_minutes=60)")
    print()
    print("3. Paginate through all results:")
    print("   items = paginate('https://api.example.com/items', results_key='data', max_pages=20)")
    print("   to_csv(items, 'all_items.csv')")
    print()
    print("4. Real example - fetch GitHub repos:")
    users = fetch("https://api.github.com/users/torvalds/repos", cache_minutes=30)
    if users:
        to_csv(users, "github_repos.csv")
        print(f"   Fetched {len(users)} repos")
