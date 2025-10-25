"""app.py

Streamlit app that draws the sky and checks ISS passes. Minimal UX and alert subscription.
"""

import streamlit as st
from sky_tools import get_positions, plot_sky
from event_detector import next_iss_pass
from notifier import send_email_alert

st.set_page_config(page_title='Real-Time Sky Tracker', page_icon='🌌')
st.title('🌌 Real-Time Sky Tracker (Python Starter)')

st.markdown('Simple demo: realtime positions (Sun, Moon, Mars, Jupiter) + ISS pass detector.')

col1, col2 = st.columns([2,1])
with col1:
    lat = st.number_input('Latitude', value=40.7128, format='%.6f')
    lon = st.number_input('Longitude', value=-74.0060, format='%.6f')
    if st.button('Refresh Sky'):
        positions = get_positions(lat, lon)
        buf, fig = plot_sky(positions)
        st.image(buf)

with col2:
    st.subheader('ISS Alerts')
    min_alt = st.slider('Min visible altitude (deg)', 5, 60, 10)
    lookahead = st.slider('Lookahead hours', 1, 12, 6)
    if st.button('Check next ISS pass'):
        result = next_iss_pass(lat, lon, min_alt_deg=min_alt, lookahead_hours=lookahead)
        if result:
            st.success(f"Next pass start: {result['start_utc']} (peak {result['peak_utc']}, alt {result['peak_alt_deg']:.1f}°)")
            email = st.text_input('Email (optional): enter to receive a one-time alert')
            if email:
                try:
                    send_email_alert('ISS pass alert', f"Next ISS pass: start {result['start_utc']}, peak {result['peak_utc']}, peak alt {result['peak_alt_deg']:.1f}°.", email)
                    st.info('Email sent!')
                except Exception as e:
                    st.error(f'Failed to send email: {e}')
        else:
            st.warning('No visible ISS passes found in the lookahead window.')

st.markdown('---')
st.info('This is a starter app. For production: refresh TLEs frequently, secure credentials, and add user accounts and push notifications.')
