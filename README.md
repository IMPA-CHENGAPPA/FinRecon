# FinRecon – Financial Transaction Reconciliation System

## About the Project
FinRecon is a web-based financial reconciliation application developed using Python and Django. It compares bank transactions with internal financial records and identifies discrepancies automatically.

## Features
- Upload bank and internal transaction CSV files.
- Automatically compare transaction IDs and amounts.
- Identify matched and mismatched transactions.
- Detect missing records.
- View reconciliation results on a dashboard.
- Search and filter exceptions.
- Update exception status and add notes.
- Download reconciliation reports in CSV format.

## Technologies Used
- Python
- Django
- Pandas
- SQLite
- HTML
- CSS

## How to Run

1. Clone the repository.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Apply migrations:
   `python manage.py migrate`
4. Start the server:
   `python manage.py runserver`
5. Open `http://127.0.0.1:8000/` in your browser.

## Project Structure
- `config/` – Django project settings.
- `reconciliation/` – Application logic and models.
- `templates/` – HTML pages.
- `manage.py` – Django management file.

## Future Enhancements
- Advanced analytics and visualizations.
- User authentication.
- More detailed financial reports.

**Project Type:** Academic Portfolio Project