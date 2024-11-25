import json
import os
from datetime import datetime
from pprint import pprint

import duckdb

con = duckdb.connect("workouts.db")

con.sql("CREATE SEQUENCE IF NOT EXISTS seq_workout_type_id START 1;");
con.sql("""
        CREATE TABLE IF NOT EXISTS workout_type (
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_workout_type_id'),
            name VARCHAR
        )
""")

# conn.commit()
gym_map = {}
con.execute(
    "Select gym_brand.name, gym.name, gym.id from gym_brand join gym on gym.brand_id=gym_brand.id;"
)
gyms = con.fetchall()
for gym in gyms:
    if gym_map.get(gym[0]) == None:
        gym_map[gym[0]] = {gym[1]: gym[2]}
    else:
        gym_map[gym[0]][gym[1]] = gym[2]
        


day_map = {}
con.execute("Select name, id from workout_type;")
days = con.fetchall()
for day in days:
    day_map[day[0]] = day[1]
    


excers_set = {}


counter = 0
with open("notes.txt", "r") as file:
    content = file.read()
workouts = content.split("\n\n\n")

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
    
    sets = 0
    reps = 0
    weight = 0

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
                for exc in excers:
                    exc = exc.strip("\n").split("\n")
                    exc_name = exc[0].strip().lower()
                    exc_name_parts = exc_name.split(" - ")
                    if len(exc_name_parts) == 1:
                        # excers_set[exc_name] = {
                        #     "Workout": exc_name_parts[0],
                        #     "Equipment": exc_name_parts[1].split(' / '),
                        #     "Position": exc_name_parts[2].split(' / '),
                        # }
                        # if exc_name == '':
                        #     print(f"Empty excersize: {date}")
                        # for sets in exc[1:]:
                        #     sets = sets.split(" x ")
                        excers_set[exc_name] = {
                            "Workout": "",
                            "Equipment": "",
                            "Position": "",
                        }
            else:
                print(f"Day not found: {date}")
    counter += 1

# workouts = []
# equipment = []
# positions = []
# for exc in excers_set:
#     workouts.append(excers_set[exc]["Workout"])
#     equipment += excers_set[exc]["Equipment"]
#     positions += excers_set[exc]["Position"]
# workouts = list(set(workouts))
# equipment = list(set(equipment))
# positions = list(set(positions))
# workouts.sort()
# equipment.sort()
# positions.sort()
# pprint(workouts)
# pprint(equipment)
# pprint(positions)

sorted = list(excers_set.keys())
sorted.sort()
pprint(sorted)
print(len(sorted))

with open("excersizes.json", "w") as myfile:
    myfile.write(json.dumps(excers_set))
with open("excerlist.json", "w") as myfile:
    myfile.write(json.dumps(sorted))


# conn.commit()
con.close()
