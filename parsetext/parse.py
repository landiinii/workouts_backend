import json

import duckdb
from addParts.days import days_main
from addParts.gyms import gyms_main
from addParts.workouts import workouts_main
from addParts.exercises import exercises_main

con = duckdb.connect("workouts.db")

with open("notes.txt", "r") as file:
    content = file.read()

gym_map = gyms_main(con)
day_map = days_main(con)
workout_map = workouts_main(con, content, gym_map, day_map)
exercises_main(con, workout_map)

with open("workouts.json", "w") as file:
    file.write(json.dumps(workout_map, indent=4))
    
con.commit()
con.close()
