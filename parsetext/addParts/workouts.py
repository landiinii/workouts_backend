from datetime import datetime


def build_tables(con):
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_workout_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS workout (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_workout_id'),
                workout_type_id SMALLINT REFERENCES workout_type(id),
                gym_id SMALLINT REFERENCES gym(id),
                date DATE
            );
    """)
  
def populate_tables(con, content, gym_map, day_map):    
    workouts = content.split("\n\n\n")

    wrk_map = {}
    for wks in workouts:
        wks = wks.strip()
        if wks == "":
            continue

        wks = wks.split("\n")
        date_string = wks[0][-8:]
        date = datetime.strptime(date_string, "%m-%d-%y")

        gym_day = date_string = wks[0][:-8]
        gym = gym_day.split(" ")[0]
        city = gym_day.split(" ")[1]
        day = " ".join(gym_day.split(" ")[2:]).strip()

        if gym in gym_map:
            if city in gym_map[gym]:
                gym_id = gym_map[gym][city]
                if day in day_map:
                    day_id = day_map[day]
                    con.execute(
                        "Select id from workout where date = ? and gym_id = ? and workout_type_id = ?;",
                        (
                            date.date(),
                            gym_id,
                            day_id,
                        ),
                    )
                    workout_id = con.fetchone()
                    if workout_id == None:
                        con.execute(
                            "INSERT INTO workout(date, gym_id, workout_type_id) VALUES(?, ?, ?) RETURNING id;",
                            (date, gym_id, day_id),
                        )
                        workout_id = con.fetchone()
                    excers = "\n".join(wks[1:]).strip().split("\n\n")
                    excers_map = {}
                    for exc in excers:
                        exc = exc.split("\n")
                        if exc[0] in excers_map:
                            print(f"Duplicate exercise: {exc[0]}, {date}")
                        excers_map[exc[0]] = exc[1:]
                    wrk_map[workout_id[0]] = excers_map
            
                else:
                    print(f"Day not found: {date}")
            else:
                print(f"City not found: {date}")
        else:
            print(f"Gym not found: {date}")
    return wrk_map

def workouts_main(con, content, gym_map, day_map):
    build_tables(con)
    return populate_tables(con, content, gym_map, day_map)
