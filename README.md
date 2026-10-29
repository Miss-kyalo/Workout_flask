# Workout Tracking API

A beginner-friendly Flask API for creating workouts and reusable exercises.
Each workout can include multiple exercises with set, rep, or duration details.

## Requirements

- Python 3.8 or newer
- Pipenv

## Install

From the project directory, create the virtual environment and install the
packages listed in `Pipfile`:

```bash
pipenv install
```

Set up the database tables with Flask-Migrate. Run `db init` only the first
time you set up the project:

```bash
pipenv run flask --app server.app db init
pipenv run flask --app server.app db migrate -m "create workout tables"
pipenv run flask --app server.app db upgrade
```

Load example workouts and exercises:

```bash
pipenv run python -m server.seed
```

The seed command resets the workout data and inserts examples each time it is
run.

## Run

```bash
pipenv run python -m server.app
```

The API runs at `http://127.0.0.1:5555`.

## Endpoints

All request and response bodies use JSON.

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/workouts` | List workouts and their exercise details. |
| `GET` | `/workouts/<id>` | Show one workout and its exercises, sets, reps, or duration. |
| `POST` | `/workouts` | Create a workout. JSON: `{"name": "Strength", "description": "Optional"}` |
| `DELETE` | `/workouts/<id>` | Delete a workout and its workout-exercise rows. |
| `GET` | `/exercises` | List exercises. |
| `GET` | `/exercises/<id>` | Show one exercise and the workouts that use it. |
| `POST` | `/exercises` | Create an exercise. JSON: `{"name": "Squat", "muscle_group": "Legs"}` |
| `DELETE` | `/exercises/<id>` | Delete an exercise and its workout-exercise rows. |
| `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. JSON must include at least one of `sets`, `reps`, or `duration_seconds`, for example `{"sets": 3, "reps": 10}`. |

Names must be non-empty and unique. Set, rep, and duration values must be
positive. Invalid requests return a JSON error with status `400`; duplicate
names or adding the same exercise to a workout twice returns status `409`.

## Tests

Run the API tests with Python's built-in test runner:

```bash
pipenv run python -m unittest discover -s tests -v
```