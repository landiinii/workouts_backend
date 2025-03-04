import streamlit as st
from data.duckdb_conn import DuckDBConnection

def construct_excercises_query(equipment=[], position=[], muscle_group=[]):
    params = []
    equipment_str = ', '.join(["?"] * len(equipment))
    params.extend(equipment)
    position_str = ', '.join(["?"] * len(position))
    params.extend(position)
    muscle_group_str = ', '.join(["?"] * len(muscle_group))
    params.extend(muscle_group)
    
    query = """
        SELECT e.name AS exercise_name,
        FROM
            exercise_set es
        JOIN movement e ON es.movement_id = e.id
        JOIN equipment_set eseq ON es.id = eseq.set_id
        JOIN equipment eq ON eseq.equipment_id = eq.id
        JOIN position_set es_p ON es.id = es_p.set_id
        JOIN position p ON es_p.position_id = p.id
        JOIN movement_muscle_group mmg ON e.id = mmg.movement_id
        JOIN muscle_group mg ON mmg.muscle_group_id = mg.id
        WHERE 1 = 1
    """
    if equipment:
        query += f"AND eq.name in ({equipment_str})\n"
    if position:
        query += f"AND p.name in ({position_str})\n"
    if muscle_group:
        query += f"AND mg.name in ({muscle_group_str})\n"
        
    query += """
        GROUP BY
            e.name
        ORDER BY
            max(es.weight) DESC;
    """

dd_conn = DuckDBConnection()


# Title
st.title("Catalog")
st.write("This is the Catalog page.")

# Filters
equipment = []
position = []
muscle_group = []

# Query the database
query = construct_excercises_query(equipment, position, muscle_group)
workout_data = dd_conn.query(query)

st.write("### Exercise Catalog")
st.dataframe(workout_data, hide_index=True)

dd_conn.close()


