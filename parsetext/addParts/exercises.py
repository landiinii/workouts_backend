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
    
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_position_set_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS position_set (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_position_set_id'),
                set_id INTEGER REFERENCES exercise_set(id),
                position_id SMALLINT REFERENCES position(id),
            )
    """)
    
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_equipment_set_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS equipment_set (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_equipment_set_id'),
                set_id INTEGER REFERENCES exercise_set(id),
                equipment_id SMALLINT REFERENCES equipment(id),
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
        """
            DELETE from position_set where set_id in (
                SELECT id from exercise_set where workout_id = ?
            );
        """,
        (workout_id,),
    )
    con.execute(
        """
            DELETE from equipment_set where set_id in (
                SELECT id from exercise_set where workout_id = ?
            );
        """,
        (workout_id,),
    )
    con.execute(
        "DELETE from exercise_set where workout_id = ?;",
        (workout_id,),
    )

def position_set(con, set_id, position_ids):
    valid_position_sets = []
    for position_id in position_ids:
        con.execute(
            "SELECT id from position_set where set_id = ? and position_id = ?;",
            (set_id, position_id,),
        )
        position_set_id = con.fetchone()
        if position_set_id == None:
            con.execute(
                "INSERT INTO position_set(set_id, position_id) VALUES(?, ?) RETURNING id;",
                (set_id, position_id,),
            )
            position_set_id = con.fetchone()
        valid_position_sets.append(position_set_id[0])
    
    # Delete any position_sets that are not in valid_position_sets
    query = "DELETE from position_set where set_id = ? and id not in (" + ",".join(["?"] * len(valid_position_sets)) + ");"
    valid_position_sets.insert(0, set_id)
    con.execute(
        query,
        valid_position_sets,
    )

def equipment_set(con, set_id, equipment_ids):
    valid_equipment_sets = []
    for equipment_id in equipment_ids:
        con.execute(
            "SELECT id from equipment_set where set_id = ? and equipment_id = ?;",
            (set_id, equipment_id,),
        )
        equipment_set_id = con.fetchone()
        if equipment_set_id == None:
            con.execute(
                "INSERT INTO equipment_set(set_id, equipment_id) VALUES(?, ?) RETURNING id;",
                (set_id, equipment_id,),
            )
            equipment_set_id = con.fetchone()
        valid_equipment_sets.append(equipment_set_id[0])
    
    # Delete any equipment_set that are not in valid_equipment_set
    query = "DELETE from equipment_set where set_id = ? and id not in (" + ",".join(["?"] * len(valid_equipment_sets)) + ");"
    valid_equipment_sets.insert(0, set_id)
    con.execute(
        query,
        valid_equipment_sets,
    )

def populate_tables(con, workout_map):
    for workout_key in workout_map.keys():
        workout = workout_map[workout_key]
        truncate_workout(con, workout_key)
        for exercise in workout.keys():
            movement, equipment, position = exercise.split(" - ")
            
            movement_id = get_movement_id(con, movement)
            
            position_ids = []
            for pos in position.split(" / "):
                position_ids.append(get_position_id(con, pos))
            
            equipment_ids = []
            for eqp in equipment.split(" / "):
                equipment_ids.append(get_equipment_id(con, eqp))
            
            for set in workout[exercise]:
                set = set.split("x")
                weight = set[0].strip()
                reps = set[1].strip()
                repeats = set[2].strip() if len(set) == 3 else '1'
                if weight.isnumeric() and reps.isnumeric() and repeats.isnumeric(): 
                    for i in range(int(repeats)):
                        con.execute(
                            "INSERT INTO exercise_set(workout_id, movement_id, weight, reps) VALUES(?, ?, ?, ?) RETURNING id;",
                            (workout_key, movement_id, int(weight), int(reps)),
                        )
                        set_id = con.fetchone()[0]
                        position_set(con, set_id, position_ids)
                        equipment_set(con, set_id, equipment_ids)
                        
                        
                        
                else:
                    print("Error Non Numeric Set: ", workout_key, movement_id, weight, reps, repeats)

            
            


                
def exercises_main(con, workout_map):
    build_tables(con)
    populate_tables(con, workout_map)
    