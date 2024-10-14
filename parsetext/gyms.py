import duckdb

con = duckdb.connect("workouts.db")


gym_map = {
    "Valhalla": {"AF": {}},
    "EOS": {"Orem": {}},
    "Vasa": {"AF": {}, "Saratoga": {}, "Herriman": {}, "Provo": {}, "Lindon": {}},
    "Rec_Center": {"Provo_Fieldhouse": {}, "Snow_College": {}},
    "Vacation": {
        "Jungle_Gym_Tulum_Beach": {},
        "Jungle_Gym_Tulum_City": {},
        "Ukiyo_Hawaii": {},
        "Sonnys_USVI": {},
    },
    "Competition": {
        "Bishop_Barbell": {},
        "Fitcon": {},
        "The_Compound": {},
        "Highland_Fling": {},
        "Brazen_Gathering": {},
        "Sinister_Games": {},
    },
    "Hotel_Gym": {"Pune": {}, "Hawaii": {}, "Las_Vegas_Flamingo": {}},
    "Home_Gym": {"Bryans": {}},
    "Work_Gym": {"Innovation_Point": {}},
}

for gym in gym_map:
    con.execute("Select id from gym_brand where name = ?;", (gym,))
    brand_id = con.fetchone()
    if brand_id == None:
        con.execute("INSERT INTO gym_brand(name) VALUES(?) RETURNING id;", (gym,))
        brand_id = con.fetchone()
    for city in gym_map[gym]:
        con.execute(
            "Select id from gym where name = ? and brand_id = ?;",
            (
                city,
                brand_id[0],
            ),
        )
        gym_id = con.fetchone()
        if gym_id == None:
            con.execute(
                "INSERT INTO gym(name, brand_id) VALUES(?, ?) RETURNING id;",
                (city, brand_id[0]),
            )
            gym_id = con.fetchone()
        print(gym_id)
        
        
con.table("gym_brand").show()
con.table("gym").show()