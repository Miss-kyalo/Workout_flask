from server.app import app
from server.models import Exercise, Workout, WorkoutExercise, db


with app.app_context():
    db.drop_all()
    db.create_all()

    strength = Workout(
        name="Full Body Strength", description="A beginner-friendly strength workout."
    )
    cardio = Workout(name="Quick Cardio", description="A short cardio session.")

    squat = Exercise(
        name="Bodyweight Squat",
        muscle_group="Legs",
        description="A simple lower-body exercise.",
    )
    push_up = Exercise(
        name="Push-Up",
        muscle_group="Chest",
        description="A bodyweight upper-body exercise.",
    )
    jumping_jack = Exercise(
        name="Jumping Jack",
        muscle_group="Full body",
        description="A cardio warm-up exercise.",
    )

    db.session.add_all([strength, cardio, squat, push_up, jumping_jack])
    db.session.flush()
    db.session.add_all(
        [
            WorkoutExercise(workout=strength, exercise=squat, sets=3, reps=10),
            WorkoutExercise(workout=strength, exercise=push_up, sets=3, reps=8),
            WorkoutExercise(
                workout=cardio, exercise=jumping_jack, duration_seconds=60
            ),
        ]
    )
    db.session.commit()
    print("Database reset and example workouts added.")
