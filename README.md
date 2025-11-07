# Hospital Appointment Manager

A simple hospital appointment manager built with Python and Streamlit. Use this app to register patients and doctors, schedule appointments, view and edit records, and reset the database. A demo data seeder is included to quickly populate the app for testing.

## Features
- Add / view / edit / delete patients
- Add / view / edit / delete doctors
- Schedule, view, edit, and cancel appointments
- Simple SQLite database (hospital.db)
- Dashboard with quick stats
- Demo data seeder available from the Dashboard

## Prerequisites
- Windows, macOS or Linux with Python 3.8+
- Git (optional)

Recommended: create and use a virtual environment for this project.

## Quick setup (Windows PowerShell)

1. Clone the repository (if you haven't already)

```powershell
git clone https://github.com/hemant0hack/Hospital-Appointment-Manager.git
cd Hospital-Appointment-Manager
```

2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies

```powershell
.venv\Scripts\pip.exe install -r requirements.txt
```

If you don't have a `requirements.txt`, at minimum install:

```powershell
.venv\Scripts\pip.exe install streamlit pandas
```

## Run the app

Start the Streamlit app using the virtual environment's Streamlit executable:

```powershell
.venv\Scripts\streamlit.exe run "$(Resolve-Path .\app.py)"
```

Open the URL printed by Streamlit (usually http://localhost:8501) in your browser.

## Seed demo data

To quickly add sample patients, doctors and appointments for testing:

1. Open the app and go to the Dashboard.
2. Expand the **Demo / Test data** section.
3. Click **Seed demo data** — the app will insert a few sample patients, doctors and appointments (it will skip any records with existing IDs).

After seeding, use the `All Patients`, `All Doctors` and `All Appointments` views to confirm the data.

## Database

- The app uses a local SQLite database file named `hospital.db` (created in the project directory by the `HospitalDatabase` class).
- If you need to inspect the database manually, you can use tools like `sqlite3`, DB Browser for SQLite, or a Python script.

## Troubleshooting
- If success messages don't appear or the UI doesn't update immediately after an action, try switching tabs or refreshing the browser page. The app reads the database on interaction and will show the latest data.
- If Streamlit errors mention missing attributes like `experimental_rerun` or `rerun`, update Streamlit to a modern version or run the app without programmatic reruns (the app is compatible with multiple Streamlit versions).

## Development notes
- Main app: `app.py`
- Database wrapper: `database.py` (uses SQLite)
## License
This project includes a `LICENSE` file — check it for licensing details.

## Contribution
Feel free to open issues or submit pull requests with improvements or bug fixes.

---
Made with ❤️ — Hospital Appointment Manager by Hemant Rathore
