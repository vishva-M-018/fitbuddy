# FitBuddy Phase-wise Implementation Checklist

This file maps the supplied FitBuddy project documentation to the implementation.

## Milestone 1 — Model Selection and Architecture

### Activity 1.1 — Select the Generative AI model
Document requirement:
- Workout generation and plan updates use a Pro-class Gemini model.
- Nutrition/recovery uses a Flash-class Gemini model.

Implementation:
- `app/gemini_generator.py` -> `settings.workout_model`
- `app/updated_plan.py` -> `settings.workout_model`
- `app/gemini_flash_generator.py` -> `settings.fast_model`
- Model IDs are configurable through `.env`.

Current defaults:
- Workout/update: `gemini-3.1-pro`
- Fast tip: `gemini-3.8-flash`

The original document names Gemini 1.5 Pro and Gemini Flash. Those are preserved
as the architectural roles, while current model IDs are configurable rather than
hard-coded to retired model names.

### Activity 1.2 — Define architecture
Implemented:
- Frontend: Jinja2 HTML templates
- Backend: FastAPI
- AI layer: Google Gemini API
- Database: SQLite + SQLAlchemy

### Activity 1.3 — Development environment
Implemented:
- `requirements.txt`
- `.env.example`
- virtual-environment instructions in `README.md`
- Uvicorn startup command
- `/docs` API documentation

---

## Milestone 2 — Core Functionality

### Activity 2.1 — Core functions
Implemented:
- `generate_workout_gemini()` in `app/gemini_generator.py`
- `generate_nutrition_tip_with_flash()` in `app/gemini_flash_generator.py`
- `update_workout_plan()` in `app/updated_plan.py`
- `save_user()`, `save_plan()`, `update_plan()`, `get_original_plan()`,
  `get_user()` in `app/database.py`

### Activity 2.2 — FastAPI backend
Implemented in `app/routes.py`:
- form input
- Pydantic validation
- Gemini calls
- database persistence
- feedback update
- template rendering

---

## Milestone 3 — routes.py

Implemented routes:

1. `GET /`
   - Shows `index.html`

2. `POST /generate-workout`
   - Validates user data
   - Calls workout Gemini function
   - Calls nutrition/recovery Gemini function
   - Saves user
   - Saves plan
   - Shows `result.html`

3. `POST /submit-feedback`
   - Finds the saved user and plan
   - Sends original plan + feedback to Gemini
   - Saves revised plan
   - Shows updated result

4. `GET /view-all-users`
   - Loads all users and plans
   - Shows `all_users.html`

5. `POST /delete-user`
   - Deletes a user only when the configured admin token matches

---

## Milestone 4 — Frontend

### Activity 4.1
Implemented:
- `templates/index.html`
- `templates/result.html`
- `templates/all_users.html`
- `templates/base.html`
- `static/css/style.css`

The interface contains:
- name
- user ID
- age
- weight
- goal
- intensity
- generated 7-day plan
- nutrition/recovery tip
- feedback form
- admin plan display

### Activity 4.2
Jinja2 is used to bind backend values to HTML:
- `{{ user.username }}`
- `{{ user.goal }}`
- `{{ workout_plan }}`
- `{{ nutrition_tip }}`
- `{% for user in users %}`

---

## Milestone 5 — Deployment

Implemented:
- virtual environment setup
- `pip install -r requirements.txt`
- `.env` configuration
- Uvicorn local deployment
- SQLite automatic initialization
- `/health`
- `/docs`
- automated `pytest` smoke tests

---

## Scope limits

The application intentionally stays within the supplied project scope:
- no unnecessary React/Node frontend
- no unnecessary external database
- no authentication system beyond the documented local admin token
- no extra AI agents
- no image-generation subsystem
- no unrelated APIs
- no paid cloud deployment requirement

The Gemini model selection is the only part intentionally modernized because
the supplied document specifies older model names. The role separation remains
the same.
