import unittest

from server.app import app
from server.models import WorkoutExercise, db


class WorkoutApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        with app.app_context():
            db.drop_all()
            db.create_all()
        self.client = app.test_client()

    def test_create_and_view_workout_with_exercise_details(self):
        workout_response = self.client.post(
            "/workouts", json={"name": "Strength", "description": "First workout"}
        )
        exercise_response = self.client.post(
            "/exercises",
            json={"name": "Squat", "muscle_group": "Legs"},
        )
        workout_id = workout_response.get_json()["id"]
        exercise_id = exercise_response.get_json()["id"]

        association_response = self.client.post(
            f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
            json={"sets": 3, "reps": 10},
        )

        self.assertEqual(workout_response.status_code, 201)
        self.assertEqual(exercise_response.status_code, 201)
        self.assertEqual(association_response.status_code, 201)
        details = self.client.get(f"/workouts/{workout_id}").get_json()
        self.assertEqual(details["workout_exercises"][0]["sets"], 3)
        self.assertEqual(
            details["workout_exercises"][0]["exercise"]["name"], "Squat"
        )

    def test_rejects_invalid_data_and_duplicate_association(self):
        self.assertEqual(
            self.client.post("/workouts", json={"name": "  "}).status_code, 400
        )
        self.assertEqual(
            self.client.post(
                "/exercises", json={"name": "Squat", "muscle_group": " "}
            ).status_code,
            400,
        )

        workout_id = self.client.post(
            "/workouts", json={"name": "Strength"}
        ).get_json()["id"]
        exercise_id = self.client.post(
            "/exercises", json={"name": "Squat", "muscle_group": "Legs"}
        ).get_json()["id"]
        path = (
            f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises"
        )

        self.assertEqual(self.client.post(path, json={}).status_code, 400)
        self.assertEqual(
            self.client.post(path, json={"sets": 3, "reps": 10}).status_code, 201
        )
        self.assertEqual(
            self.client.post(path, json={"duration_seconds": 30}).status_code, 409
        )

    def test_deleting_workout_deletes_join_rows(self):
        workout_id = self.client.post(
            "/workouts", json={"name": "Strength"}
        ).get_json()["id"]
        exercise_id = self.client.post(
            "/exercises", json={"name": "Squat", "muscle_group": "Legs"}
        ).get_json()["id"]
        self.client.post(
            f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
            json={"sets": 2},
        )

        self.assertEqual(
            self.client.delete(f"/workouts/{workout_id}").status_code, 204
        )
        with app.app_context():
            self.assertEqual(WorkoutExercise.query.count(), 0)

    def test_missing_workout_returns_not_found(self):
        self.assertEqual(self.client.get("/workouts/999").status_code, 404)


if __name__ == "__main__":
    unittest.main()
