from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class BasicWorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String(allow_none=True)


class BasicExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    muscle_group = fields.String()
    description = fields.String(allow_none=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    exercise = fields.Nested(BasicExerciseSchema, dump_only=True)
    sets = fields.Integer(
        allow_none=True, validate=validate.Range(min=1, error="Sets must be positive.")
    )
    reps = fields.Integer(
        allow_none=True, validate=validate.Range(min=1, error="Reps must be positive.")
    )
    duration_seconds = fields.Integer(
        allow_none=True,
        validate=validate.Range(min=1, error="Duration must be positive."),
    )

    @validates_schema
    def require_a_workout_goal(self, data, **kwargs):
        if not any(data.get(key) is not None for key in ("sets", "reps", "duration_seconds")):
            raise ValidationError(
                "Provide at least one of sets, reps, or duration_seconds."
            )


class WorkoutExerciseWorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout = fields.Nested(BasicWorkoutSchema, dump_only=True)
    sets = fields.Integer(allow_none=True)
    reps = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True, validate=validate.Length(min=1, max=80)
    )
    description = fields.String(allow_none=True, validate=validate.Length(max=255))
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema, many=True, dump_only=True
    )

    @validates_schema
    def require_nonblank_name(self, data, **kwargs):
        if not data.get("name", "").strip():
            raise ValidationError({"name": ["Workout name cannot be empty."]})


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True, validate=validate.Length(min=1, max=80)
    )
    muscle_group = fields.String(
        required=True, validate=validate.Length(min=1, max=50)
    )
    description = fields.String(allow_none=True, validate=validate.Length(max=255))
    workout_exercises = fields.Nested(
        WorkoutExerciseWorkoutSchema, many=True, dump_only=True
    )

    @validates_schema
    def require_nonblank_fields(self, data, **kwargs):
        errors = {}
        if not data.get("name", "").strip():
            errors["name"] = ["Exercise name cannot be empty."]
        if not data.get("muscle_group", "").strip():
            errors["muscle_group"] = ["Muscle group cannot be empty."]
        if errors:
            raise ValidationError(errors)
