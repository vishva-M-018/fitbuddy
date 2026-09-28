from typing import Literal

from pydantic import BaseModel, Field, field_validator


Goal = Literal["weight loss", "muscle gain", "general wellness", "flexibility", "endurance"]
Intensity = Literal["low", "medium", "high"]


class UserInput(BaseModel):
    username: str = Field(min_length=1, max_length=120)
    user_id: str = Field(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9_-]+$")
    age: int = Field(ge=13, le=120)
    weight: float = Field(gt=0, le=500)
    goal: Goal
    intensity: Intensity

    @field_validator("username")
    @classmethod
    def clean_username(cls, value: str) -> str:
        return " ".join(value.split()).strip()


class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=80)
    feedback: str = Field(min_length=3, max_length=2000)
