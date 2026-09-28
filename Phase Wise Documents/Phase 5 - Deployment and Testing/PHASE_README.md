# Phase 5 — Deployment and Testing

Study:
- `project/README.md` — setup and run commands
- `project/requirements.txt` — Python dependencies
- `project/.env.example` — safe configuration template
- `project/tests/test_app.py` — smoke tests
- `project/app/main.py` — `/health` and application startup
- `project/.gitignore` — keeps `.env`, database and generated files out of Git

Run from the `project` folder:
1. Create/activate `.venv`.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your own API key.
4. `uvicorn app.main:app --reload`
5. `pytest -q`

The complete application is included so this phase can still be run from VS Code.
