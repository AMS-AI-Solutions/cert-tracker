# Cert-Tracker

Cert-Tracker is a minimal MVP for tracking certificate expiration dates. It provides both a command‑line interface (CLI) for quick checks and a web API for future integration with a React frontend.

---

## Tech Stack

* **Python & UV**: version management, dependency pinning, virtualenv
* **FastAPI**: HTTP API with automatic Swagger docs
* **Uvicorn**: ASGI server for development and production
* **Pandas**: CSV parsing and date filtering
* **Typer**: CLI support for the `check` command
* **python-dotenv**: manage environment variables via `.env` files
* **python-multipart**: handle file uploads in FastAPI

**Dev tools**

* **pytest**: unit testing framework
* **ruff**: linting and auto‑fixes
* **mypy**: static type checking

---

## Project Structure

```text
cert-tracker/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── services.py        # CSV parsing & expiration logic
│   │   ├── models.py          # Pydantic schemas
│   │   ├── cli.py             # Typer-based CLI (check command)
│   │   └── __init__.py
│   └── data/
│       └── sample_certs.csv   # Sample CSV for testing
├── uploads/                   # Runtime: user-uploaded files
├── frontend/                  # React/TS/Vite/Material UI app
├── .env                       # Environment variables (gitignored)
├── pyproject.toml             # Python project config
├── .gitignore                 # ignores logs, uploads/, etc.
└── README.md
```

---

## Prerequisites

* **uv** CLI ([https://github.com/astral-sh/uv](https://github.com/astral-sh/uv))
* Python 3.12+
* (Optional) Node.js & npm/yarn for frontend

---

## Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-org/cert-tracker.git
   cd cert-tracker
   ```

2. **Python setup with UV**

   ```bash
   # Install & pin Python version
   uv python install 3.12
   uv python pin 3.12

   # Add & lock dependencies
   uv lock
   uv sync
   ```

3. **Frontend setup** (if working on UI)

   ```bash
   cd frontend
   npm install
   ```

4. **Environment variables** Create a `.env` in project root:

   ```dotenv
   EXPIRY_THRESHOLD_DAYS=30
   ```

---

## Usage

### 1. CLI: Check Expiring Certificates

```bash
uv run python backend/app/cli.py check \
  --input backend/data/sample_certs.csv \
  --days 30
```

This will print all certificates expiring within the next 30 days.

### 2. Web API: FastAPI Server

Run the development server with live reload:

```bash
uv run uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

* **Swagger UI:**  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Health check:**  [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 3. Save Uploaded Files

User CSV uploads are saved under the `uploads/` folder at runtime. These are ignored by Git.

---

## Testing & Linting

```bash
# Run tests
uv run pytest

# Lint & format
uv run ruff .

# Type check
uv run mypy backend/
```

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
