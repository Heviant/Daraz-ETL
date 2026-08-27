# load.py
from datetime import datetime
import duckdb


def load_data(df):
    # Connect to DuckDB (creates 'daraz.duckdb' locally)
    con = duckdb.connect("daraz.duckdb")

    # Add a timestamp column to the DataFrame before loading
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if the table 'daraz_products' exists
    table_exists = con.execute(
        """
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_name = 'daraz_products'
        """,).fetchone()[0] > 0

    if table_exists:
        # Table exists, so append the new DataFrame rows into it
        con.execute("INSERT INTO daraz_products SELECT * FROM df")
        print("Appended new data to existing table.")
    else:
        # Table does not exist, create it from the DataFrame
        con.execute("CREATE TABLE daraz_products AS SELECT * FROM df")
        print("Created new table and loaded data.")
        con.close()