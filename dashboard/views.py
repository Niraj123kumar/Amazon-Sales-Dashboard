from django.shortcuts import render
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64, json
import re

def dashboard_view(request):
    # --- Load cleaned Amazon data ---
    df = pd.read_csv("data/amazon_sales_cleaned.csv")

    # --- Clean up ---
    df.columns = df.columns.str.strip()
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    if 'Amount' in df.columns:
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df = df.dropna(subset=['Amount'])

    # --- JSON Handling Example ---
    df.to_json("data/amazon_sales.json", orient="records", lines=True)
    df_json = pd.read_json("data/amazon_sales.json", lines=True)

    # --- Regex Filtering Example (Delivered + Cancelled) ---
    delivered_or_cancelled = df[df["Status"].str.contains("Delivered|Cancelled", case=False, na=False)]

    # --- Chart 1: Monthly Sales Trend ---
    monthly_sales = (
        df.groupby(df['Date'].dt.to_period('M'))['Amount']
        .sum()
        .reset_index()
    )
    monthly_sales['Date'] = monthly_sales['Date'].astype(str)
    plt.figure(figsize=(6, 4))
    sns.lineplot(x='Date', y='Amount', data=monthly_sales, marker='o')
    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    chart1 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    buf1.close()

    # --- Chart 2: Top 5 Categories by Sales ---
    if 'Category' in df.columns:
        top_categories = df.groupby('Category')['Amount'].sum().nlargest(5)
        plt.figure(figsize=(6, 4))
        sns.barplot(x=top_categories.index, y=top_categories.values)
        plt.title("Top 5 Categories by Sales")
        plt.xticks(rotation=30)
        plt.tight_layout()
        buf2 = io.BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        chart2 = base64.b64encode(buf2.getvalue()).decode('utf-8')
        buf2.close()
    else:
        chart2 = None

    # --- Chart 3: Order Status Breakdown ---
    if 'Status' in df.columns:
        status_counts = df['Status'].value_counts()
        plt.figure(figsize=(6, 4))
        plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title("Order Status Breakdown")
        plt.tight_layout()
        buf3 = io.BytesIO()
        plt.savefig(buf3, format='png')
        buf3.seek(0)
        chart3 = base64.b64encode(buf3.getvalue()).decode('utf-8')
        buf3.close()
    else:
        chart3 = None

    # --- Chart 4: Top 5 Cities by Total Sales ---
    if 'ship-city' in df.columns:
        top_cities = df.groupby('ship-city')['Amount'].sum().nlargest(5)
        plt.figure(figsize=(6, 4))
        sns.barplot(x=top_cities.index, y=top_cities.values)
        plt.title("Top 5 Cities by Sales")
        plt.xticks(rotation=25)
        plt.tight_layout()
        buf4 = io.BytesIO()
        plt.savefig(buf4, format='png')
        buf4.seek(0)
        chart4 = base64.b64encode(buf4.getvalue()).decode('utf-8')
        buf4.close()
    else:
        chart4 = None

    # --- Chart 5: Multivariate Heatmap ---
    numeric_cols = df.select_dtypes(include='number')
    plt.figure(figsize=(6, 4))
    sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm')
    plt.title("Multivariate Correlation Heatmap")
    plt.tight_layout()
    buf5 = io.BytesIO()
    plt.savefig(buf5, format='png')
    buf5.seek(0)
    chart5 = base64.b64encode(buf5.getvalue()).decode('utf-8')
    buf5.close()

    # --- Chart 6: Pairplot (optional heavy) ---
    plt.figure()
    sample = numeric_cols.sample(min(200, len(numeric_cols))) if len(numeric_cols) > 0 else numeric_cols
    sns.pairplot(numeric_cols)
    buf6 = io.BytesIO()
    plt.savefig(buf6, format='png')
    buf6.seek(0)
    chart6 = base64.b64encode(buf6.getvalue()).decode('utf-8')
    buf6.close()

    # --- Statistical Summary ---
    summary = {
        "total_orders": len(df),
        "total_sales": round(df["Amount"].sum(), 2),
        "avg_order_value": round(df["Amount"].mean(), 2),
        "top_category": df["Category"].mode()[0] if "Category" in df.columns else "N/A",
        "top_city": df["ship-city"].mode()[0] if "ship-city" in df.columns else "N/A"
    }

    context = {
        "chart1": chart1,
        "chart2": chart2,
        "chart3": chart3,
        "chart4": chart4,
        "chart5": chart5,
        "chart6": chart6,
        "summary": summary
    }

    return render(request, "dashboard/dashboard.html", context)
