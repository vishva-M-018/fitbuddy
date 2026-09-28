from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    goal: Mapped[str] = mapped_column(String(50))
    intensity: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    plans: Mapped[list["WorkoutPlan"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="WorkoutPlan.id",
    )


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id_fk: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    original_plan: Mapped[str] = mapped_column(Text)
    updated_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    nutrition_tip: Mapped[str] = mapped_column(Text)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship(back_populates="plans")


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_user(db: Session, data) -> User:
    existing = db.query(User).filter(User.user_id == data.user_id).first()
    if existing:
        existing.username = data.username
        existing.age = data.age
        existing.weight = data.weight
        existing.goal = data.goal
        existing.intensity = data.intensity
        db.commit()
        db.refresh(existing)
        return existing

    user = User(
        user_id=data.user_id,
        username=data.username,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_plan(db: Session, user: User, plan: str, tip: str) -> WorkoutPlan:
    record = WorkoutPlan(
        user_id_fk=user.id,
        original_plan=plan,
        nutrition_tip=tip,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_user(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()


def get_original_plan(db: Session, user_id: str) -> Optional[WorkoutPlan]:
    user = get_user(db, user_id)
    if not user or not user.plans:
        return None
    return user.plans[-1]


def update_plan(db: Session, record: WorkoutPlan, updated: str, feedback: str) -> WorkoutPlan:
    record.updated_plan = updated
    record.feedback = feedback
    record.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(record)
    return record


def get_all_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.created_at.desc()).all()


def delete_user(db: Session, user_id: str) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
