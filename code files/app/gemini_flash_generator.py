from .config import settings
from .gemini_client import generate_text


def generate_nutrition_tip_with_flash(goal: str, age: int) -> str:
    prompt = f"""
Give one concise, practical nutrition or recovery tip for a FitBuddy user.
Goal: {goal}
Age: {age}

Use balanced, age-appropriate health guidance. Do not provide calorie restriction,
fasting plans, supplement prescriptions, or extreme weight-control advice.
If the user is under 18, focus on regular balanced meals, hydration, sleep and
normal growth rather than weight loss. Keep the response under 100 words.
"""
    return generate_text(settings.fast_model, prompt, max_output_tokens=300)
