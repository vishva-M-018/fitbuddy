from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .config import TEMPLATE_DIR, settings
from .database import (
    delete_user,
    get_all_users,
    get_db,
    get_original_plan,
    get_user,
    init_db,
    save_plan,
    save_user,
    update_plan,
)
from .gemini_client import GeminiUnavailable
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def render(request: Request, name: str, **context):
    return templates.TemplateResponse(
        request=request,
        name=name,
        context={"app_name": settings.app_name, **context},
    )


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return render(request, "index.html")


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
        workout = generate_workout_gemini(
            data.username, data.age, data.weight, data.goal, data.intensity
        )
        tip = generate_nutrition_tip_with_flash(data.goal, data.age)
        user = save_user(db, data)
        plan = save_plan(db, user, workout, tip)

        return render(
            request,
            "result.html",
            user=user,
            plan=plan,
            workout_plan=workout,
            nutrition_tip=tip,
            updated=False,
        )
    except (ValueError, GeminiUnavailable) as exc:
        return render(request, "index.html", error=str(exc))


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = FeedbackRequest(user_id=user_id, feedback=feedback)
        user = get_user(db, data.user_id)
        record = get_original_plan(db, data.user_id)

        if not user or not record:
            return render(
                request,
                "result.html",
                error="No saved plan was found for that User ID.",
            )

        revised = update_workout_plan(
            original_plan=record.original_plan,
            feedback=data.feedback,
            goal=user.goal,
            intensity=user.intensity,
            age=user.age,
        )
        update_plan(db, record, revised, data.feedback)

        return render(
            request,
            "result.html",
            user=user,
            plan=record,
            workout_plan=revised,
            nutrition_tip=record.nutrition_tip,
            updated=True,
        )
    except (ValueError, GeminiUnavailable) as exc:
        return render(request, "result.html", error=str(exc))


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    return render(request, "all_users.html", users=users)


@router.post("/delete-user")
def remove_user(
    request: Request,
    user_id: str = Form(...),
    admin_token: str = Form(...),
    db: Session = Depends(get_db),
):
    if admin_token != settings.admin_token:
        return HTMLResponse("Invalid admin token.", status_code=403)
    delete_user(db, user_id)
    return RedirectResponse("/view-all-users", status_code=303)
