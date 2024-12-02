day_map = {
    "Leg Day",
    "Push Day",
    "Pull Day",
    "Comp Day",
    "Strongman Day",
    "Push and Pull Day",
    "Arms Day",
    "Full Body Day",
}

def build_tables(con):
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_workout_type_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS workout_type (
                id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_workout_type_id'),
                name VARCHAR
            )
    """)

def populate_tables(con):
    for day in day_map:
        day_id = con.execute("Select id from workout_type where name = ?", (day,)).fetchone()
        if day_id == None:
            day_id = con.execute(
                "INSERT INTO workout_type(name) VALUES(?) RETURNING id", (day,)
            ).fetchone()

def fetch_days(con):
    day_map = {}
    con.execute("Select name, id from workout_type;")
    days = con.fetchall()
    for day in days:
        day_map[day[0]] = day[1]
    return day_map

def days_main(con):
    build_tables(con)
    populate_tables(con)
    return fetch_days(con)
    