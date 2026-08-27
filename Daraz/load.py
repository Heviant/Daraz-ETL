# load.py
from datetime import datetime
import duckdb


def load_data(df):
    # Connect to DuckDB (creates 'daraz.duckdb' locally)
    con = duckdb.connect("daraz.duckdb")

    # Add a timestamp column to the DataFrame before loading
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load/Append the Pandas DataFrame into a DuckDB table
    con.execute("CREATE TABLE IF NOT EXISTS daraz_products AS SELECT * FROM df")
    # If the table already exists from a previous run, use append:
    # con.execute("INSERT INTO daraz_products SELECT * FROM df")

    con.close()
    print("Data successfully transformed and loaded into DuckDB!")