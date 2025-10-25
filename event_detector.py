"""event_detector.py

Simple event detection: next visible ISS pass (coarse, checks minute-by-minute for next 6 hours).
"""

from skyfield.api import EarthSatellite, load, Topos
from tle_manager import fetch_iss_tle

def next_iss_pass(lat, lon, min_alt_deg=10, lookahead_hours=6):
    ts = load.timescale()
    tle1, tle2 = fetch_iss_tle()
    sat = EarthSatellite(tle1, tle2, 'ISS', ts)
    eph = load('de421.bsp')
    observer = eph['earth'] + Topos(latitude_degrees=lat, longitude_degrees=lon)

    t0 = ts.now()
    minutes = int(lookahead_hours * 60)
    in_pass = False
    pass_start = None
    peak_alt = 0
    peak_time = None

    for m in range(0, minutes + 1):
        t = t0 + m / (24*60)
        difference = sat - observer
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()
        altdeg = alt.degrees
        if altdeg >= min_alt_deg:
            if not in_pass:
                in_pass = True
                pass_start = t
                peak_alt = altdeg
                peak_time = t
            else:
                if altdeg > peak_alt:
                    peak_alt = altdeg
                    peak_time = t
        else:
            if in_pass:
                # pass ended; return start and peak
                return {
                    'start_utc': pass_start.utc_strftime('%Y-%m-%d %H:%M:%S UTC'),
                    'peak_utc': peak_time.utc_strftime('%Y-%m-%d %H:%M:%S UTC'),
                    'peak_alt_deg': float(peak_alt)
                }
    # If we looped without seeing a full pass
    if in_pass:
        return {
            'start_utc': pass_start.utc_strftime('%Y-%m-%d %H:%M:%S UTC'),
            'peak_utc': peak_time.utc_strftime('%Y-%m-%d %H:%M:%S UTC'),
            'peak_alt_deg': float(peak_alt)
        }
    return None
