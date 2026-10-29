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
