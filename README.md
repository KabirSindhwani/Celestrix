# Real-Time Sky Tracker (Python / Streamlit)

Minimal app that shows a simple real-time sky view (Sun, Moon, Mars, Jupiter) and detects the next visible ISS pass for a given location. Includes a simple email alert function.

## Setup
1. Clone repo or copy files into a folder.
2. Create a virtualenv and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Set environment variables for email alerts (optional):
   - `ALERT_EMAIL_FROM` - sender email (Gmail recommended with App Password)
   - `ALERT_EMAIL_PASSWORD` - SMTP password / app password

   Example (Linux/macOS):
   ```bash
   export ALERT_EMAIL_FROM="youremail@gmail.com"
   export ALERT_EMAIL_PASSWORD="your_app_password"
   ```

4. Run locally:
   ```bash
   streamlit run app.py
   ```

## Deploying to Streamlit Cloud
1. Push this repo to GitHub.
2. Create a new app on Streamlit Cloud and connect your GitHub repo.
3. Add the environment variables in the Streamlit Cloud settings.

## Notes
- This is a minimal, educational starter project. For production/higher accuracy, refresh TLEs regularly, handle rate limits, and secure secrets properly.
