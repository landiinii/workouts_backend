import duckdb

class DuckDBConnection:
    def __init__(self):
        db_path = 'data/workouts.db'
        self.con = duckdb.connect(database=db_path, read_only=True)

    def query(self, query, params=[]):
        return self.con.execute(query, params).df()
    
    def close(self):
        self.con.close()
