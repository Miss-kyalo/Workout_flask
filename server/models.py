from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates


db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"
    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="workout_name_not_empty"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))
    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True,
    )

    @validates("name")
    def validate_name(self, _key, name):
        name = name.strip()
        if not name:
            raise ValueError("Workout name cannot be empty.")
        if len(name) > 80:
            raise ValueError("Workout name must be 80 characters or fewer.")
        return name


class Exercise(db.Model):
    __tablename__ = "exercises"
    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="exercise_name_not_empty"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    muscle_group = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan"
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True,
    )

    @validates("name")
    def validate_name(self, _key, name):
        name = name.strip()
        if not name:
            raise ValueError("Exercise name cannot be empty.")
        if len(name) > 80:
            raise ValueError("Exercise name must be 80 characters or fewer.")
        return name

    @validates("muscle_group")
    def validate_muscle_group(self, _key, muscle_group):
        muscle_group = muscle_group.strip()
        if not muscle_group:
            raise ValueError("Muscle group cannot be empty.")
        if len(muscle_group) > 50:
            raise ValueError("Muscle group must be 50 characters or fewer.")
        return muscle_group


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    __table_args__ = (
        db.UniqueConstraint("workout_id", "exercise_id", name="one_exercise_per_workout"),
        CheckConstraint(
            "(sets IS NOT NULL AND sets > 0) OR "
            "(reps IS NOT NULL AND reps > 0) OR "
            "(duration_seconds IS NOT NULL AND duration_seconds > 0)",
            name="workout_exercise_has_valid_goal",
        ),
        CheckConstraint("sets IS NULL OR sets > 0", name="sets_must_be_positive"),
        CheckConstraint("reps IS NULL OR reps > 0", name="reps_must_be_positive"),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="duration_must_be_positive",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer, db.ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False
    )
    exercise_id = db.Column(
        db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False
    )
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("sets", "reps", "duration_seconds")
    def validate_positive_value(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be positive.")
        return value
