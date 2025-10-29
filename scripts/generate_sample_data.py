import pandas as pd
import os

# Path to your Amazon Sale Report
csv_path = "data/Amazon Sale Report.csv"

def load_amazon_data():
    if not os.path.exists(csv_path):
        print("❌ CSV file not found. Make sure it's inside the 'data/' folder.")
        return

    # Load the CSV
    df = pd.read_csv(csv_path)

    print("✅ Amazon Sale Report loaded successfully!")
    print("📊 Columns available:", list(df.columns))
    print("\nSample data:\n", df.head())

    # Save a cleaned copy (optional)
    df.to_csv("data/amazon_sales_cleaned.csv", index=False)
    print("\n💾 Cleaned data saved as: data/amazon_sales_cleaned.csv")

if __name__ == "__main__":
    load_amazon_data()
