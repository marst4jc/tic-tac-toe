# tic-tac-toe

A sleek Tic-Tac-Toe experience with a React-powered interface, now served through a
Django project. You play **O** while the computer opens with **X** in the center.

## Setup

Install dependencies (Python 3.9+ recommended):

```bash
python -m pip install -r requirements.txt
```

## Run the app

Start the Django development server:

```bash
python manage.py migrate  # sets up the default SQLite database
python manage.py runserver 0.0.0.0:8000
```

Open http://localhost:8000 to play the game. Static assets are served via Django's
staticfiles system.

## Configuration

Environment variables you can override:

- `DJANGO_SECRET_KEY`: custom secret key for production deployments.
- `DJANGO_DEBUG`: set to `false` to disable debug mode.
- `DJANGO_ALLOWED_HOSTS`: comma-separated list of hosts (default: `localhost,127.0.0.1`).
