from .config import settings
from .gemini_client import generate_text


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    prompt = f"""
You are FitBuddy, a cautious fitness-planning assistant.

Create a practical 7-day beginner-to-intermediate workout plan for:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Preferred intensity: {intensity}

Return exactly seven labeled days. For every day include:
- Focus
- Warm-up (5–10 minutes)
- Main workout with exercise names and sets/reps OR duration
- Rest guidance
- Cool-down/recovery

Requirements:
1. Keep recommendations general wellness guidance, not medical treatment.
2. Do not prescribe extreme exercise, starvation, dehydration, supplements, or unsafe challenges.
3. Do not give calorie targets or restrictive dieting advice.
4. Include at least one recovery/rest-focused day.
5. If the user is under 18, emphasize age-appropriate movement, gradual progression,
   rest, hydration, and normal balanced meals; do not discuss weight-loss dieting.
6. Mention that pain, dizziness, injury, or medical concerns are reasons to stop and
   seek guidance from a parent/guardian or qualified healthcare professional.
7. Keep the plan clear enough to follow from a phone screen.
"""
    return generate_text(settings.workout_model, prompt, max_output_tokens=5000)
