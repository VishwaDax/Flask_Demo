# Flask PostgreSQL Auth Example

Minimal Flask app using SQLAlchemy with PostgreSQL.

## Prerequisites

- Python 3.8+
- PostgreSQL server
- Virtual environment (recommended)

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Configure database

You can set a single `DATABASE_URL` or individual Postgres vars.

Example `DATABASE_URL` (PowerShell):

```powershell
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/users_db"
```

Or set individual variables:

```powershell
$env:POSTGRES_USER = "postgres"
$env:POSTGRES_PASSWORD = "postgres"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "5432"
$env:POSTGRES_DB = "users_db"
```

Create the database (using `psql`):

```powershell
psql -U postgres -h localhost -c "CREATE DATABASE users_db;"
```

Or with `createdb`:

```powershell
createdb -U postgres users_db
```

## Run the app

```powershell
python app.py
```

On startup the app calls `db.create_all()` to create the `users` table if missing.

## Migrations (optional but recommended)

After installing dependencies, initialize and run migrations with the Flask CLI:

```powershell
$env:FLASK_APP = "app.py"
flask db init
flask db migrate -m "initial"
flask db upgrade
```

If `flask` is not found, ensure your virtual environment is activated.

## Files

- [app.py](app.py) — main Flask app
- [requirements.txt](requirements.txt) — Python dependencies

## Notes

- If you deploy to platforms that provide `DATABASE_URL` with the `postgres://` scheme, the app normalizes it to `postgresql://` for SQLAlchemy compatibility.
- For production, consider adding `Flask-Migrate` (Alembic) and using proper secrets management for credentials.

---

If you want, I can add Flask-Migrate and example migration commands next.
