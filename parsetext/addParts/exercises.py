def build_tables(con):
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_movement_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS movement (
                id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_movement_id'),
                name VARCHAR
            )
    """)
    
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_muscle_group_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS muscle_group (
                id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_muscle_group_id'),
                name VARCHAR
            )
    """)
    
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_movement_muscle_group_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS movement_muscle_group (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_movement_muscle_group_id'),
                movement_id SMALLINT REFERENCES movement(id),
                muscle_group_id SMALLINT REFERENCES muscle_group(id),
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

def get_muscle_group_names(movement):
    movement_muscle_groups = {
        "Ab Rollouts": [
            "Abs",
            "Obliques",
            "Lower Back"
        ],
        "Arnold Press": [
            "Shoulders",
            "Biceps",
            "Triceps"
        ],
        "Back Extension": [
            "Lower Back",
            "Glutes",
            "Hamstrings"
        ],
        "Banded Clam": [
            "Glutes",
            "Hip Abductors"
        ],
        "Bench Press": [
            "Chest",
            "Triceps",
            "Shoulders"
        ],
        "Bicep Curl": [
            "Biceps"
        ],
        "Block Pull": [
            "Lats",
            "Back",
            "Hamstrings",
            "Glutes",
            "Legs",
            "Posterior Chain"
        ],
        "Calf Raise": [
            "Calves"
        ],
        "Carry": [
            "Full Body",
            "Forearms",
            "Shoulders",
            "Core"
        ],
        "Chest": [
            "Chest"
        ],
        "Clean and Press": [
            "Full Body",
            "Legs",
            "Back",
            "Shoulders",
            "Arms"
        ],
        "Crunch": [
            "Abs"
        ],
        "Deadhang": [
            "Forearms",
            "Shoulders",
            "Back"
        ],
        "Deadlift": [
            "Back",
            "Legs",
            "Glutes",
            "Hamstrings",
            "Core"
        ],
        "Dip": [
            "Triceps",
            "Chest",
            "Shoulders"
        ],
        "Drag": [
            "Full Body",
            "Legs",
            "Back",
            "Arms"
        ],
        "Extension": [
            "Triceps"
        ],
        "Face Pulls": [
            "Shoulders",
            "Upper Back",
            "Rear Delts"
        ],
        "Field Goal": [
            "Shoulders"
        ],
        "Fingal Finger": [
            "Full Body",
            "Legs",
            "Back",
            "Shoulders"
        ],
        "Fire Hydrant": [
            "Glutes",
            "Hip Abductors"
        ],
        "Fly": [
            "Chest",
            "Shoulders"
        ],
        "French Press": [
            "Triceps"
        ],
        "GHR": [
            "Hamstrings",
            "Glutes",
            "Lower Back"
        ],
        "Good Morning": [
            "Lower Back",
            "Hamstrings",
            "Glutes"
        ],
        "Hip Abductor": [
            "Glutes",
            "Hip Abductors"
        ],
        "Hip Adductor": [
            "Inner Thighs"
        ],
        "Hip Thrust": [
            "Glutes",
            "Hamstrings",
            "Lower Back"
        ],
        "Hold": [
            "Full Body",
            "Core",
            "Forearms"
        ],
        "Kicks": [
            "Legs",
            "Glutes"
        ],
        "Leg Curl": [
            "Hamstrings"
        ],
        "Leg Extension": [
            "Quadriceps"
        ],
        "Leg Press": [
            "Legs",
            "Quadriceps",
            "Glutes"
        ],
        "Leg Raise": [
            "Abs",
            "Hip Flexors"
        ],
        "Leg raise": [
            "Abs",
            "Hip Flexors"
        ],
        "Load": [
            "Full Body",
            "Legs",
            "Back"
        ],
        "Log Clean": [
            "Full Body",
            "Legs",
            "Back"
        ],
        "Log Press": [
            "Shoulders",
            "Triceps"
        ],
        "Lunges": [
            "Legs",
            "Glutes"
        ],
        "Monster Walk": [
            "Glutes",
            "Hip Abductors"
        ],
        "OHP": [
            "Shoulders",
            "Triceps"
        ],
        "Pick": [
            "Full Body"
        ],
        "Plank": [
            "Abs"
        ],
        "Praise the Lord": [
            "Shoulders"
        ],
        "Pull": [
            "Back",
            "Biceps"
        ],
        "Pull Apart": [
            "Shoulders",
            "Upper Back"
        ],
        "Pull Downs": [
            "Back",
            "Biceps"
        ],
        "Pull Over": [
            "Chest",
            "Back"
        ],
        "Pull ups": [
            "Back",
            "Biceps"
        ],
        "Push": [
            "Chest",
            "Triceps"
        ],
        "Push Ups": [
            "Chest",
            "Triceps"
        ],
        "RDL": [
            "Hamstrings",
            "Glutes"
        ],
        "Rack Pull": [
            "Back",
            "Legs"
        ],
        "Raise": [
            "Shoulders"
        ],
        "Reverse Hyper": [
            "Lower Back",
            "Glutes"
        ],
        "Row": [
            "Back",
            "Biceps"
        ],
        "Russian Twists": [
            "Abs",
            "Obliques"
        ],
        "Shoulder": [
            "Shoulders"
        ],
        "Shrug": [
            "Traps"
        ],
        "Side Bend": [
            "Obliques"
        ],
        "Skull Crusher": [
            "Triceps"
        ],
        "Squat": [
            "Legs",
            "Glutes"
        ],
        "Stair Climb": [
            "Legs",
            "Glutes"
        ],
        "Step Up": [
            "Legs",
            "Glutes"
        ],
        "Swing": [
            "Full Body"
        ],
        "Throw": [
            "Full Body"
        ],
        "Tire flips": [
            "Full Body"
        ],
        "Toes to Bar": [
            "Abs"
        ],
        "Tricep Extensions": [
            "Triceps"
        ],
        "Tricep Press": [
            "Triceps"
        ],
        "Wall Sit": [
            "Legs"
        ],
        "Wheelbarrow Runs": [
            "Full Body"
        ],
        "Windmills": [
            "Abs",
            "Obliques"
        ],
        "Yoke Run": [
            "Full Body"
        ],
        "Z Press": [
            "Shoulders",
            "Triceps"
        ]
        }
    return movement_muscle_groups.get(movement, [])

def get_muscle_group_id(con, muscle_group):
    con.execute(
        "SELECT id from muscle_group where name = ?;",
        (muscle_group,),
    )
    muscle_group_id = con.fetchone()
    if muscle_group_id == None:
        con.execute(
            "INSERT INTO muscle_group(name) VALUES(?) RETURNING id;",
            (muscle_group,),
        )
        muscle_group_id = con.fetchone()
    return muscle_group_id[0]

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
        muscle_groups = get_muscle_group_names(movement)
        print(movement, muscle_groups)
        for muscle_group in muscle_groups:
            muscle_group_id = get_muscle_group_id(con, muscle_group)
            con.execute(
                "INSERT INTO movement_muscle_group(movement_id, muscle_group_id) VALUES(?, ?);",
                (movement_id[0], muscle_group_id),
            )
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
    