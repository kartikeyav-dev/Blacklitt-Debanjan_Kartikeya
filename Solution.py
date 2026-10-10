import time
from pathlib import Path
import requests

URL = ("https://nsearchives.nseindia.com/products/content/"
       "sec_bhavdata_full_{d:%d%m%Y}.csv")
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "text/csv,*/*",
           "Referer": "https://www.nseindia.com/"}


def fetch_day(d, raw_dir: Path, session: requests.Session):
    """Download one day's full bhavcopy once; return its path or None."""
    out = raw_dir / f"sec_bhavdata_full_{d:%Y%m%d}.csv"
    if out.exists():
        return out                          # cached: never download twice
    for attempt in range(4):
        r = session.get(URL.format(d=d), headers=HEADERS, timeout=30)
        if r.status_code == 200 and r.content:
            out.write_bytes(r.content)
            time.sleep(1.0)                 
            return out
        if r.status_code == 404:
            return None                     # holiday or not published
        time.sleep(2 ** attempt)            # back off and retry
    raise RuntimeError(f"download failed for {d:%Y-%m-%d}")