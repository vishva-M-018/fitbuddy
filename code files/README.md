# FitBuddy – AI Fitness Plan Generator

A complete FastAPI + Jinja2 + SQLite + SQLAlchemy + Gemini project based on the
provided FitBuddy project documentation.

## Features

- User profile form: name, user ID, age, weight, goal and intensity
- AI-generated 7-day workout plan
- AI-generated nutrition/recovery tip
- Feedback-based plan regeneration
- SQLite persistence
- Admin/local dashboard showing users and original/updated plans
- Delete-user action protected by an admin token
- FastAPI `/docs` interactive API documentation
- `/health` health-check endpoint
- Responsive HTML/CSS frontend
- Automated smoke tests

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── gemini_client.py
│   ├── gemini_flash_generator.py
│   ├── gemini_generator.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   └── updated_plan.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── all_users.html
│   ├── base.html
│   ├── index.html
│   └── result.html
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## 1. Open the project

Open the `FitBuddy` folder in VS Code.

## 2. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
py -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Create a file named `.env` by copying `.env.example`.

Put your Google Gemini API key in:

```env
GEMINI_API_KEY=your_real_key_here
```

Google AI Studio is the place to create/manage the API key.

You can also change:

```env
WORKOUT_MODEL=gemini-3.1-pro
FAST_MODEL=gemini-3.8-flash
```

if the model IDs available to your API account differ.

## 5. Start FitBuddy

From the project root:

```bash
uvicorn app.main:app --reload
```

Open:

- Website: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Admin view: http://127.0.0.1:8000/view-all-users

The SQLite database `fitbuddy.db` is created automatically.

## 6. Test the application

Run:

```bash
pytest -q
```

For a full manual test:

1. Open the home page.
2. Enter a sample profile.
3. Click **Generate 7-Day Plan**.
4. Confirm the plan and nutrition/recovery tip appear.
5. Enter feedback such as `Add more cardio and make two sessions easier`.
6. Click **Update Plan with AI**.
7. Open **Admin View**.
8. Confirm the original and updated plans are both stored.
9. Test `/docs`.
10. Test `/health`.

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | User form |
| POST | `/generate-workout` | Generate and save a plan |
| POST | `/submit-feedback` | Regenerate a plan using feedback |
| GET | `/view-all-users` | Admin/local dashboard |
| POST | `/delete-user` | Delete a user using admin token |
| GET | `/health` | Health check |
| GET | `/docs` | FastAPI Swagger UI |

## Important implementation note

The supplied project document names `Gemini 1.5 Pro`, Gemini Flash and the older
`google-generativeai` package. This implementation uses Google's current
`google-genai` SDK and makes the model IDs configurable in `.env`. The application
still preserves the document's intended separation:

- `gemini_generator.py` → full workout plan generation
- `gemini_flash_generator.py` → fast nutrition/recovery tip
- `updated_plan.py` → feedback-based plan revision

This avoids hard-coding an obsolete SDK/model choice while keeping the required
FitBuddy architecture.

## Safety and scope

FitBuddy is an educational wellness-planning demo. AI output should not be treated
as medical advice. The prompts deliberately avoid extreme exercise, starvation,
dehydration, unsafe challenges, restrictive calorie targets and supplement
prescriptions.
