import pandas as pd

def transform_product_data(raw_data):
    # Create a DataFrame from the extracted product data
    data = {
        "Product Name": [raw_data["product_name"]],
        "Product Price": [raw_data["product_price"]],
        "Product Rating": [raw_data["product_rating"]],
        "Product Count": [raw_data["product_count"]],
    }
    df = pd.DataFrame(data)

    # Perform any necessary transformations (e.g., cleaning, formatting)
    # Clean the price field if it contains currency text
    if df["Product Price"].iloc[0] != "N/A":
        df["Product Price"] = (
            df["Product Price"]
            .str.replace("Rs. ", "", regex=False)
            .str.replace(",", "")
            .astype(float)
        )
    return df