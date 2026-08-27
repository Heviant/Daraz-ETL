# main.py
from extract import search_daraz_for_product
from load import load_data
from transform import transform_product_data


def run_pipeline():
    print("--- Starting Daraz Pipeline ---")

    # 1. Extract
    print("Scraping product from Daraz...")
    raw_data = search_daraz_for_product()

    print("Raw data extracted:", raw_data)
    # 2. Transform
    print("Transforming data with Pandas...")
    clean_df = transform_product_data(raw_data)

    # 3. Load
    print("Loading data into DuckDB...")
    load_data(clean_df)

    print("--- Pipeline Completed Successfully! ---")


if __name__ == "__main__":
    run_pipeline()