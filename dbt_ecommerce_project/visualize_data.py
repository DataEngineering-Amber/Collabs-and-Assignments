# visualize_data.py — DuckDB version (no sqlalchemy)
import duckdb
import matplotlib.pyplot as plt

# Connect to local DuckDB file built by dbt
con = duckdb.connect("ecommerce.duckdb")

# Monthly revenue & orders
mro = con.execute("""
    SELECT month, total_orders, total_revenue
    FROM monthly_revenue_orders
    ORDER BY month
""").fetchdf()

plt.figure(figsize=(9,5))
plt.plot(mro["month"], mro["total_revenue"], marker="o")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Total Revenue ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_revenue.png")
plt.close()

plt.figure(figsize=(9,5))
plt.plot(mro["month"], mro["total_orders"], marker="o")
plt.title("Monthly Orders")
plt.xlabel("Month")
plt.ylabel("Total Orders")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_orders.png")
plt.close()

# Top 10 products by revenue
top_products = con.execute("""
    SELECT p.product_name, SUM(s.total_price) AS total_revenue
    FROM stg_sales s
    JOIN stg_products p USING (product_id)
    GROUP BY p.product_name
    ORDER BY total_revenue DESC
    LIMIT 10
""").fetchdf()

plt.figure(figsize=(9,6))
plt.barh(top_products["product_name"], top_products["total_revenue"])
plt.gca().invert_yaxis()
plt.title("Top 10 Products by Revenue")
plt.xlabel("Total Revenue ($)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("top_products.png")
plt.close()

print("✅ Charts saved: monthly_revenue.png, monthly_orders.png, top_products.png")
