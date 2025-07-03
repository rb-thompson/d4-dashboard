# Diablo IV Season 6 Tracker
A retro terminal-style tracker project for Diablo IV Season 9, built with Django and Plotly. Log sessions, monitor DPS, Mythics, and fun scores in real-time. A work in progress, if you play D4 and enjoy useful metrics feel free to suggest ideas or contribute!

## Features
- Live session logging with skill and Paragon tracking
- DPS trend and fun score charts

## Setup
1. Clone repo: `git clone <repo-url>`
2. Create virtual env: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
4. Install deps: `pip install -r requirements.txt`
5. Migrate DB: `python manage.py migrate`
6. Run: `python manage.py runserver`

## Usage
- Log sessions via the form
- View metrics and charts on the dashboard

## Tech
- Django 5.2.4
- Plotly
- Tailwind CSS

## License
MIT