import duckdb

con = duckdb.connect("workouts.db")

con.sql("CREATE SEQUENCE IF NOT EXISTS seq_gym_brand_id START 1;");
con.sql("""
        CREATE TABLE IF NOT EXISTS gym_brand (
            id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_gym_brand_id'),
            name VARCHAR
        )
""")

con.sql("CREATE SEQUENCE IF NOT EXISTS seq_gym_id START 1;");
con.sql("""
        CREATE TABLE IF NOT EXISTS gym (
            id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_gym_id'),
            name VARCHAR,
            brand_id SMALLINT REFERENCES gym_brand(id),
        )
""")


con.sql("CREATE SEQUENCE IF NOT EXISTS seq_workout_type_id START 1;");
con.sql("""
        CREATE TABLE IF NOT EXISTS workout_type (
            id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_workout_type_id'),
            name VARCHAR
        )
""")

con.sql("CREATE SEQUENCE IF NOT EXISTS seq_workout_id START 1;");
con.sql("""
        CREATE TABLE IF NOT EXISTS workout (
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_workout_id'),
            workout_type_id SMALLINT REFERENCES workout_type(id),
            gym_id SMALLINT REFERENCES gym(id),
            date DATE
        );
""")
