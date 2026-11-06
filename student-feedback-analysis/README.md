# Student Feedback Analysis System

A beginner-friendly Flask + MySQL project for collecting anonymous course ratings and displaying aggregate feedback analytics.

## Features
- Anonymous course feedback (no student account or identity fields)
- 1–5 rating validation
- Course-wise and question-wise averages
- Response counts and rating distribution
- Matplotlib charts and CSV export
- Parameterized SQL queries

## Requirements
- Python 3.10+
- MySQL Server 8+
- Git

## Setup (Windows PowerShell)

1. Extract the project ZIP and open the project folder in VS Code.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create the database and sample courses/questions. In MySQL Workbench, open `database/schema.sql` and execute it. Or use the MySQL command line:

   ```powershell
   mysql -u root -p < database/schema.sql
   ```

5. Copy `.env.example` to `.env` and edit the MySQL password:

   ```powershell
   Copy-Item .env.example .env
   ```

6. Start the app:

   ```powershell
   python app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env, then run database/schema.sql in MySQL
python app.py
```

## Pages
- `/` Home page
- `/feedback` Submit feedback
- `/dashboard` Aggregated analytics
- `/export` Download course summary CSV

## Run tests

```bash
pytest
```

## Push to GitHub

Create an empty repository on GitHub, then run these commands in the project folder:

```bash
git init
git add .
git commit -m "Initial commit: Student Feedback Analysis System"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/student-feedback-analysis.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Never commit `.env`, database passwords, student identities, or raw identifiable feedback.

## Privacy and limitations
- This starter app intentionally does not collect names, emails, or student IDs.
- Free-text comments are stored but never shown on the dashboard or included in exports.
- For a real deployment, consider suppressing small groups (for example, fewer than 5 responses), adding admin authentication, CSRF protection, rate limiting, retention controls, and secure hosting.
- The included dashboard is a teaching/demo dashboard, not a production-secured admin portal.
