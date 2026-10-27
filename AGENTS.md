# AGENTS.md

## Stack
- Django 6.1.2, Python >=3.14.7 (see `pyproject.toml`)
- Project package: `config/` (settings/urls/wsgi/asgi). Settings module: `config.settings` (set in `manage.py`).
- DB: SQLite at `db.sqlite3` (BASE_DIR). Email uses console backend.
- Deps managed with `uv` (`uv.lock` present).

## Commands (run from repo root)
```bash
# Install/sync deps
uv sync

# Run dev server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Shell/admin
python manage.py shell
python manage.py createsuperuser

# Tests
python manage.py test
```

## Notes
- `INSTALLED_APPS` has only Django defaults (no custom apps yet). Add apps to `config/settings.py` when created.
- `ROOT_URLCONF = 'config.urls'`, `WSGI_APPLICATION = 'config.wsgi.application'`.
- No existing `AGENTS.md`/`README`/CI/lint/test configs found; follow Django defaults unless you add tools.
