CREATE TABLE "workout_type" (
  "id" smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "name" character varying(32)
);

CREATE TABLE "gym_brand" (
  "id" smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "name" character varying(32)
);

CREATE TABLE "gym" (
  "id" smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "name" character varying(64),
  "brand_id" smallint,
  CONSTRAINT "FK_gym.brand_id"
    FOREIGN KEY ("brand_id")
      REFERENCES "gym_brand"("id")
);

CREATE TABLE "workout" (
  "id" integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "workout_type_id" smallint,
  "gym_id" smallint,
  "created_at" timestamp without time zone DEFAULT now(),
  "updated_at" timestamp without time zone DEFAULT now(),
  "date" date,
  CONSTRAINT "FK_workout.gym_id"
    FOREIGN KEY ("gym_id")
      REFERENCES "gym"("id"),
  CONSTRAINT "FK_workout.workout_type_id"
    FOREIGN KEY ("workout_type_id")
      REFERENCES "workout_type"("id")
);

CREATE TABLE "set" (
  "id" integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "workout_id" integer,
  "excercise_id" smallint,
  "weight" smallint,
  "reps" smallint,
  "rpe" smallint,
  CONSTRAINT "FK_set.workout_id"
    FOREIGN KEY ("workout_id")
      REFERENCES "workout"("id")
);

CREATE TABLE "exercise" (
  "id" smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "name" character varying(128)
);

CREATE TABLE "muscle" (
  "id" smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "name" character varying(64)
);

CREATE TABLE "muscle_group" (
  "id" integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "exercise_id" smallint,
  "muscle_id" smallint,
  CONSTRAINT "FK_muscle_group.exercise_id"
    FOREIGN KEY ("exercise_id")
      REFERENCES "exercise"("id"),
  CONSTRAINT "FK_muscle_group.muscle_id"
    FOREIGN KEY ("muscle_id")
      REFERENCES "muscle"("id")
);
