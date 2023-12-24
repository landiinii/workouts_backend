import os
from datetime import datetime
from pprint import pprint

import psycopg2

passwd = os.getenv("db_password")
if passwd == None:
    print("add the password for database to env")
    exit()

conn = psycopg2.connect(
    database="workouts",
    user="postgres",
    password=passwd,
    host="workouts.cc8sc0sxljmc.us-west-2.rds.amazonaws.com",
    port="5432",
)
cursor = conn.cursor()


# gym_map = {
#     "Valhalla": {"AF": {}},
#     "EOS": {"Orem": {}},
#     "Vasa": {"AF": {}, "Saratoga": {}, "Herriman": {}, "Provo": {}, "Lindon": {}},
#     "Rec_Center": {"Provo_Fieldhouse": {}, "Snow_College": {}},
#     "Vacation": {
#         "Jungle_Gym_Tulum_Beach": {},
#         "Jungle_Gym_Tulum_City": {},
#         "Ukiyo_Hawaii": {},
#         "Sonnys_USVI": {},
#     },
#     "Competition": {
#         "Bishop_Barbell": {},
#         "Fitcon": {},
#         "The_Compound": {},
#         "Highland_Fling": {},
#         "Brazen_Gathering": {},
#         "Sinister_Games": {},
#     },
#     "Hotel_Gym": {"Pune": {}, "Hawaii": {}, "Las_Vegas_Flamingo": {}},
#     "Home_Gym": {"Bryans": {}},
#     "Work_Gym": {"Innovation_Point": {}},
# }

# day_map = {
#     "Leg Day",
#     "Push Day",
#     "Pull Day",
#     "Comp Day",
#     "Strongman Day",
#     "Push and Pull Day",
#     "Arms Day",
#     "Full Body Day",
# }

# for day in day_map:
#     cursor.execute("Select id from workout_type where name = %s;", (day,))
#     day_id = cursor.fetchone()
#     if day_id == None:
#         cursor.execute(
#             "INSERT INTO workout_type(name) VALUES(%s) RETURNING id;", (day,)
#         )
#         day_id = cursor.fetchone()
#     print(day_id)

# for gym in gym_map:
#     cursor.execute("Select id from gym_brand where name = %s;", (gym,))
#     brand_id = cursor.fetchone()
#     if brand_id == None:
#         cursor.execute("INSERT INTO gym_brand(name) VALUES(%s) RETURNING id;", (gym,))
#         brand_id = cursor.fetchone()
#     for city in gym_map[gym]:
#         cursor.execute(
#             "Select id from gym where name = %s and brand_id = %s;",
#             (
#                 city,
#                 brand_id[0],
#             ),
#         )
#         gym_id = cursor.fetchone()
#         if gym_id == None:
#             cursor.execute(
#                 "INSERT INTO gym(name, brand_id) VALUES(%s, %s) RETURNING id;",
#                 (city, brand_id[0]),
#             )
#             gym_id = cursor.fetchone()
#         print(gym_id)

# conn.commit()
gym_map = {}
cursor.execute(
    "Select gym_brand.name, gym.name, gym.id from gym_brand join gym on gym.brand_id=gym_brand.id;"
)
gyms = cursor.fetchall()
for gym in gyms:
    if gym_map.get(gym[0]) == None:
        gym_map[gym[0]] = {gym[1]: gym[2]}
    else:
        gym_map[gym[0]][gym[1]] = gym[2]

day_map = {}
cursor.execute("Select name, id from workout_type;")
days = cursor.fetchall()
for day in days:
    day_map[day[0]] = day[1]


excers_set = set()


counter = 0
with open("notes.txt", "r") as file:
    content = file.read()
workouts = content.split("\n\n\n")

for wks in workouts:
    wks = wks.strip()
    if wks == "":
        continue

    wks = wks.split("\n")
    date_string = wks[0][-5:] + "-23"
    date = datetime.strptime(date_string, "%m-%d-%y")

    gym_day = date_string = wks[0][:-5]
    gym = gym_day.split(" ")[0]
    city = gym_day.split(" ")[1]
    day = " ".join(gym_day.split(" ")[2:]).strip()

    if gym in gym_map:
        if city in gym_map[gym]:
            gym_id = gym_map[gym][city]
            if day in day_map:
                day_id = day_map[day]
                cursor.execute(
                    "Select id from workout where date = %s and gym_id = %s and workout_type_id = %s;",
                    (
                        date.date(),
                        gym_id,
                        day_id,
                    ),
                )
                workout_id = cursor.fetchone()
                if workout_id == None:
                    cursor.execute(
                        "INSERT INTO workout(date, gym_id, workout_type_id) VALUES(%s, %s, %s) RETURNING id;",
                        (date, gym_id, day_id),
                    )
                    workout_id = cursor.fetchone()
                    print(gym, city, day, workout_id)
                # add excersizes here
        else:
            print(gym, city, wks[0])
            continue
    else:
        print(gym, wks[0])
        continue

    # excers = "\n".join(wks[1:]).strip().split("\n\n")
    # for exc in excers:
    #     exc = exc.strip("\n")
    #     exc = exc.split("\n")
    #     excers_set.add(exc[0])

    counter += 1

# sorted = list(excers_set)
# sorted.sort()
# print("\n".join(sorted))


conn.commit()
conn.close()
