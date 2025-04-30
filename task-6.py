import pandas as pd
import sqlite3

# Step 1: Load the CSV
df = pd.read_csv("Auto Sales data.csv")

# Step 2: Convert order_date to datetime (if needed)
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

# Step 3: Connect to SQLite DB (or create one)
conn = sqlite3.connect("sales.db")

# Step 4: Write to SQLite table
df.to_sql("orders", conn, if_exists="replace", index=False)

# Step 5: Run SQL for monthly revenue and order volume
query = """
SELECT
    strftime('%Y',ORDERDATE) AS year,
    strftime('%m', ORDERDATE) AS month,
    SUM(PRICEEACH) AS total_revenue,
    COUNT(DISTINCT ORDERNUMBER) AS order_volume
FROM orders
GROUP BY year, month
ORDER BY year, month;
"""

result_df = pd.read_sql_query(query, conn)

# Step 6: Show results
print(result_df)

# Optionally save to CSV
result_df.to_csv("monthly_sales_trend.csv", index=False)

conn.close()
print("Script started")
