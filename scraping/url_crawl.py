import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE_URL = "https://fastapi.tiangolo.com/"
START_PATH = "python-types/"
STOP_PATH = "how-to/authentication-error-status-code/"

urls = [START_PATH]          # store ONLY relative paths
visited = set()

def to_relative(url: str) -> str:
    """Convert absolute FastAPI URL to relative path"""
    if url.startswith(BASE_URL):
        return url.replace(BASE_URL, "")
    return url

while True:
    current = urls[-1]

    # stop if already processed
    if current in visited:
        break

    visited.add(current)

    current_abs = urljoin(BASE_URL, current)
    response = requests.get(current_abs)
    soup = BeautifulSoup(response.text, "html.parser")

    # ---------- 1️⃣ Canonical handling ----------
    canonical_tag = soup.find("link", rel="canonical")
    if canonical_tag:
        canonical_rel = to_relative(canonical_tag.get("href"))

        # stop immediately if canonical is the stop page
        if canonical_rel == STOP_PATH:
            urls.append(canonical_rel)
            break

        # jump to canonical if new
        if canonical_rel and canonical_rel not in visited:
            urls.append(canonical_rel)
            continue

    # ---------- 2️⃣ Next page handling ----------
    next_tag = soup.find("link", rel="next")
    if not next_tag:
        break

    # resolve relative URLs correctly
    next_abs = urljoin(current_abs, next_tag.get("href"))
    next_rel = to_relative(next_abs)

    # append next page
    urls.append(next_rel)

    # stop immediately after adding final allowed page
    if next_rel == STOP_PATH:
        break

# ---------- Save output ----------
with open("url.json", "w") as f:
    json.dump(urls, f, indent=4)

print(f"Collected {len(urls)} URLs")
print("Last URL:", urls[-1])
