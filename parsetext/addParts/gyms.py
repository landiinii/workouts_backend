gym_map = {
    "Valhalla": {"AF": {}},
    "EOS": {"Orem": {}},
    "Vasa": {"AF": {}, "Saratoga": {}, "Herriman": {}, "Provo": {}, "Lindon": {}, "University": {}},
    "Rec_Center": {"Provo_Fieldhouse": {}, "Snow_College": {}},
    "Vacation": {
        "Jungle_Gym_Tulum_Beach": {},
        "Jungle_Gym_Tulum_City": {},
        "Ukiyo_Hawaii": {},
        "Sonnys_USVI": {},
        "Iron_Legacy_Barbell": {},
        "Alphaland": {},
    },
    "Competition": {
        "Bishop_Barbell": {},
        "Fitcon": {},
        "The_Compound": {},
        "Highland_Fling": {},
        "Brazen_Gathering": {},
        "Sinister_Games": {},
        "Stones_of_Strength": {},
        "Viking_Power": {},
        "Bailey_Family_Reunion": {},
        "Welsh_Days": {},
    },
    "Hotel_Gym": {"Pune": {}, "Hawaii": {}, "Las_Vegas_Flamingo": {}, "Baner": {}},
    "Home_Gym": {"Bryans": {}},
    "Work_Gym": {"Innovation_Point": {}, "Redo_Office": {}},
}

def build_tables(con):
    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_gym_brand_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS gym_brand (
                id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_gym_brand_id'),
                name VARCHAR
            )
    """)

    con.sql("CREATE SEQUENCE IF NOT EXISTS seq_gym_id START 1;");
    con.sql("""
            CREATE TABLE IF NOT EXISTS gym (
                id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('seq_gym_id'),
                name VARCHAR,
                brand_id SMALLINT REFERENCES gym_brand(id),
            )
    """)

def populate_tables(con):
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

def fetch_gyms(con):
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
    return gym_map
                    
def gyms_main(con):
    build_tables(con)
    populate_tables(con)
    return fetch_gyms(con)
    