def build_tables(con):
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_movement_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS movement (
                id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_movement_id'),
                name VARCHAR
            )
    """)
    
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_position_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS position (
                id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_position_id'),
                name VARCHAR
            )
    """)
    
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_equipment_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS equipment (
                id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_equipment_id'),
                name VARCHAR
            )
    """)
    
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_exercise_set_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS exercise_set (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_exercise_set_id'),
                workout_id INTEGER REFERENCES workout(id),
                movement_id SMALLINT REFERENCES movement(id),
                weight SMALLINT,
                reps SMALLINT,
                warmup BOOLEAN DEFAULT FALSE,
            )
    """)

def get_movement_id(con, movement):
    con.execute(
        "SELECT id from movement where name = ?;",
        (movement,),
    )
    movement_id = con.fetchone()
    if movement_id == None:
        con.execute(
            "INSERT INTO movement(name) VALUES(?) RETURNING id;",
            (movement,),
        )
        movement_id = con.fetchone()
    return movement_id[0]

def get_position_id(con, position):
    con.execute(
        "SELECT id from position where name = ?;",
        (position,),
    )
    position_id = con.fetchone()
    if position_id == None:
        con.execute(
            "INSERT INTO position(name) VALUES(?) RETURNING id;",
            (position,),
        )
        position_id = con.fetchone()
    return position_id[0]

def get_equipment_id(con, equipment):
    con.execute(
        "SELECT id from equipment where name = ?;",
        (equipment,),
    )
    equipment_id = con.fetchone()
    if equipment_id == None:
        con.execute(
            "INSERT INTO equipment(name) VALUES(?) RETURNING id;",
            (equipment,),
        )
        equipment_id = con.fetchone()
    return equipment_id[0]

def truncate_workout(con, workout_id):
    con.execute(
        "DELETE from exercise_set where workout_id = ?;",
        (workout_id,),
    )

def populate_tables(con, workout_map):
    for workout_key in workout_map.keys():
        workout = workout_map[workout_key]
        truncate_workout(con, workout_key)
        for exercise in workout.keys():
            movement, equipment, position = exercise.split(" - ")
            movement_id = get_movement_id(con, movement)
            for set in workout[exercise]:
                set = set.split("x")
                weight = set[0].strip()
                reps = set[1].strip()
                repeats = set[2].strip() if len(set) == 3 else '1'
                if weight.isnumeric() and reps.isnumeric() and repeats.isnumeric(): 
                    for i in range(int(repeats)):
                        con.execute(
                            "INSERT INTO exercise_set(workout_id, movement_id, weight, reps) VALUES(?, ?, ?, ?);",
                            (workout_key, movement_id, int(weight), int(reps)),
                        )
                else:
                    print("Error Non Numeric Set: ", workout_key, movement_id, weight, reps, repeats)

            
            position_ids = []
            for pos in position.split(" / "):
                position_ids.append(get_position_id(con, pos))
            
            equipment_ids = []
            for eqp in equipment.split(" / "):
                equipment_ids.append(get_equipment_id(con, eqp))


                
def exercises_main(con, workout_map):
    build_tables(con)
    populate_tables(con, workout_map)
    