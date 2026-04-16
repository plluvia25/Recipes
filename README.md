# Recetas (GenAI) — Run locally and install on iPad

Minimal instructions to run this Streamlit-based recipe app locally, make it easy to add to an iPad Home Screen, and push the project to GitHub.

Getting started (Windows / PowerShell)

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
python -m pip install -U pip
python -m pip install -r requirements.txt
```

3. Run the app (Streamlit)

```powershell
streamlit run main.py
```

Open the printed Local URL (usually `http://localhost:8501`) in Safari on your iPad. To have an app-like experience, use Safari's Share → Add to Home Screen. This creates an icon that launches the app in a standalone window.

Notes about iPad support

- This project uses Streamlit (server + browser). It is not a native iOS app and does not include a full PWA manifest/service-worker. That said, modern iPad Safari supports "Add to Home Screen" which gives a near-app experience.
- If you want a native iPad app (App Store / TestFlight), the recommended paths are:
  - Reimplement UI in SwiftUI (native) — best performance and App Store distribution.
  - Use a webview wrapper (e.g., Capacitor) pointing to a hosted version of this app — easier but still requires an Apple Developer account.

Prepare and push to GitHub (PowerShell)

```powershell
# Initialize repo (if not already initialized)
 git init
 # Add all files and commit
 git add .
 git commit -m "Initial commit: recetas app"
 # Create repo on GitHub (use gh CLI or create via web) then push
 # Example using GitHub CLI (install https://cli.github.com/):
 # gh repo create <your-username>/recetas --public --source=. --remote=origin --push
 # OR add remote manually and push:
 # git remote add origin https://github.com/<your-username>/recetas.git
 # git branch -M main
 # git push -u origin main
```

Basic CI (GitHub Actions)

This repo includes a simple workflow that installs dependencies and runs a Python syntax check. See `.github/workflows/ci.yml`.

If you want, I can:
- Add a small PWA manifest and service-worker and adapt the app to serve them (limited for Streamlit).
- Create a hosted deployment (e.g., Streamlit Community Cloud, Heroku, or Render) and add instructions.
- Prepare a native iPad wrapper (Capacitor or Swift skeleton) and repository layout for Xcode.

Tell me which of the above you'd like next (PWA + hosted, or native iPad build), and I'll proceed.
