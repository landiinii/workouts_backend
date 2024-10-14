import duckdb

con = duckdb.connect("workouts.db")


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

for day in day_map:
    day_id = con.execute("Select id from workout_type where name = ?", (day,)).fetchone()
    if day_id == None:
        day_id = con.execute(
            "INSERT INTO workout_type(name) VALUES(?) RETURNING id", (day,)
        ).fetchone()
    print(day_id)

con.table("workout_type").show()
con.close()