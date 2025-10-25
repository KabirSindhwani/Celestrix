"""sky_tools.py

Functions to compute alt/az for some solar system bodies and to draw a simple polar sky map using matplotlib.
"""

from skyfield.api import load, Topos
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# Keep a single ephemeris download per process
_EPHEMERIS = None
_TS = None

def _load_ephem():
    global _EPHEMERIS, _TS
    if _EPHEMERIS is None:
        _EPHEMERIS = load('de421.bsp')
        _TS = load.timescale()
    return _EPHEMERIS, _TS

def get_positions(lat, lon):
    """Return alt/az for some bodies at current time for observer lat/lon (decimal degrees).
    Returns dict: { 'Sun': {'alt':..,'az':..}, ... }
    """
    eph, ts = _load_ephem()
    t = ts.now()
    earth = eph['earth']
    bodies = {
        'Sun': eph['sun'],
        'Moon': eph['moon'],
        'Mars': eph['mars'],
        'Jupiter': eph['jupiter barycenter']
    }
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    out = {}
    for name, body in bodies.items():
        astrometric = observer.observe(body).apparent()
        alt, az, _ = astrometric.altaz()
        out[name] = {'alt': float(alt.degrees), 'az': float(az.degrees)}
    return out

def plot_sky(data):
    """Plot a simple polar sky map (Matplotlib Figure). Returns BytesIO of PNG and the matplotlib Figure."""
    fig = plt.figure(figsize=(6,6), facecolor='black')
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor('black')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0,90)
    ax.set_yticklabels([])

    for name, vals in data.items():
        az = np.radians(vals['az'])
        alt = 90 - vals['alt']
        ax.scatter(az, alt, s=80, alpha=0.9)
        ax.text(az, alt, f' {name}', color='white', fontsize=10, ha='left', va='bottom')

    ax.grid(color='gray', alpha=0.3)
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf, fig
