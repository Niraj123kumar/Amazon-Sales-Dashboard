import pandas as pd
import sqlite3
import os

# Define paths
data_path = "data"
db_path = "ecommerce.db"

# Check if data exists
for file in ["customers.csv", "products.csv", "orders.csv"]:
    if not os.path.exists(os.path.join(data_path, file)):
        raise FileNotFoundError(f"Missing file: {file}. Run generate_sample_data.py first.")

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect(db_path)
print("✅ Connected to SQLite database")

# Load CSVs into pandas DataFrames
customers = pd.read_csv(os.path.join(data_path, "customers.csv"))
products = pd.read_csv(os.path.join(data_path, "products.csv"))
orders = pd.read_csv(os.path.join(data_path, "orders.csv"))

# Write tables to database
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)

# Close connection
conn.close()

print("✅ Data imported into ecommerce.db successfully!")
