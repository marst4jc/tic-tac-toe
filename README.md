# tic-tac-toe

A sleek Tic-Tac-Toe experience with a React-powered interface, now served through a
Django project. You play **O** while the computer opens with **X** in the center.

## Setup

This repository includes a tiny, built-in Django-compatible stub so it can run
without downloading external packages (the execution environment does not allow
network access).

## Run the app

Start the lightweight development server (only `runserver` is implemented in the
stub; migrations/admin are intentionally unavailable):

```bash
python manage.py runserver 0.0.0.0:8000
```

Open http://localhost:8000 to play the game. Static assets are served via Django's
staticfiles system.

## Configuration

Environment variables you can override:

- `DJANGO_SECRET_KEY`: custom secret key for production deployments.
- `DJANGO_DEBUG`: set to `false` to disable debug mode.
- `DJANGO_ALLOWED_HOSTS`: comma-separated list of hosts (default: `localhost,127.0.0.1`).
