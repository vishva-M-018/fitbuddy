from .config import settings
from .gemini_client import generate_text


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str,
    age: int,
) -> str:
    prompt = f"""
You are updating a FitBuddy 7-day workout plan.

Goal: {goal}
Intensity: {intensity}
Age: {age}

Original plan:
---BEGIN ORIGINAL---
{original_plan}
---END ORIGINAL---

User feedback:
---BEGIN FEEDBACK---
{feedback}
---END FEEDBACK---

Return a complete revised seven-day plan, not a list of changes.
Apply reasonable parts of the feedback while preserving safety and the user's goal.

Rules:
- Keep warm-up, main workout, rest/recovery and cool-down guidance.
- Do not introduce extreme exercise, dehydration, starvation, unsafe challenges,
  calorie restriction or supplement prescriptions.
- For users under 18, do not turn the plan into a weight-loss diet or aggressive
  body-composition program.
- Include a short safety note about stopping for pain, dizziness or injury.
"""
    return generate_text(settings.workout_model, prompt, max_output_tokens=5000)
