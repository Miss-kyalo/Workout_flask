from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.models import Exercise, Workout, WorkoutExercise, db
from server.schemas import ExerciseSchema, WorkoutExerciseSchema, WorkoutSchema


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

workout_schema = WorkoutSchema()
exercise_schema = ExerciseSchema()
workout_exercise_schema = WorkoutExerciseSchema()


def invalid_json_response():
    return jsonify({"errors": {"_schema": ["Request body must be valid JSON."]}}), 400


@app.get("/workouts")
def list_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return jsonify(workout_schema.dump(workouts, many=True))


@app.get("/workouts/<int:workout_id>")
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return jsonify({"error": "Workout not found."}), 404
    return jsonify(workout_schema.dump(workout))


@app.post("/workouts")
def create_workout():
    body = request.get_json(silent=True)
    if body is None:
        return invalid_json_response()
    try:
        data = workout_schema.load(body)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    workout = Workout(**data)
    db.session.add(workout)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A workout with that name already exists."}), 409
    return jsonify(workout_schema.dump(workout)), 201


@app.delete("/workouts/<int:workout_id>")
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return jsonify({"error": "Workout not found."}), 404
    db.session.delete(workout)
    db.session.commit()
    return "", 204


@app.get("/exercises")
def list_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercise_schema.dump(exercises, many=True))


@app.get("/exercises/<int:exercise_id>")
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404
    return jsonify(exercise_schema.dump(exercise))


@app.post("/exercises")
def create_exercise():
    body = request.get_json(silent=True)
    if body is None:
        return invalid_json_response()
    try:
        data = exercise_schema.load(body)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    exercise = Exercise(**data)
    db.session.add(exercise)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An exercise with that name already exists."}), 409
    return jsonify(exercise_schema.dump(exercise)), 201


@app.delete("/exercises/<int:exercise_id>")
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404
    db.session.delete(exercise)
    db.session.commit()
    return "", 204


@app.post(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises"
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return jsonify({"error": "Workout not found."}), 404
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404
    if WorkoutExercise.query.filter_by(
        workout_id=workout_id, exercise_id=exercise_id
    ).first():
        return jsonify({"error": "This exercise is already in the workout."}), 409

    body = request.get_json(silent=True)
    if body is None:
        return invalid_json_response()
    try:
        data = workout_exercise_schema.load(body)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    workout_exercise = WorkoutExercise(
        workout=workout, exercise=exercise, **data
    )
    db.session.add(workout_exercise)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Could not add the exercise to this workout."}), 409
    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
