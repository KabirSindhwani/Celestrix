"""tle_manager.py

Simple TLE fetcher with a small fallback. For production use, refresh frequently and consider Space-Track/Celestrak policies.
"""

import requests

CELESTRAK_ISS_URL = 'https://celestrak.org/NORAD/elements/stations.txt'

FALLBACK_ISS_TLE = (
    '1 25544U 98067A   25298.54774306  .00019087  00000-0  35417-3 0  9991',
    '2 25544  51.6418 127.3330 0008267  93.2067  29.4623 15.50285140383756'
)

def fetch_iss_tle(timeout=10):
    """Try to fetch the ISS TLE from Celestrak. Return (line1, line2) or fallback."""
    try:
        r = requests.get(CELESTRAK_ISS_URL, timeout=timeout)
        r.raise_for_status()
        text = r.text.splitlines()
        # stations.txt contains blocks: name, line1, line2
        # find 'ISS (ZARYA)' block
        for i, line in enumerate(text):
            if 'ISS' in line or 'ZARYA' in line:
                if i + 2 < len(text):
                    return text[i+1].strip(), text[i+2].strip()
        # fallback to first TLE-looking lines
        for i in range(len(text)-2):
            if text[i+1].startswith('1 ') and text[i+2].startswith('2 '):
                return text[i+1].strip(), text[i+2].strip()
    except Exception:
        pass
    return FALLBACK_ISS_TLE
