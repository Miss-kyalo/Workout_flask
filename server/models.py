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
