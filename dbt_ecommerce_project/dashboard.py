# dashboard.py — one image with 3 charts + a small table
import duckdb
import matplotlib.pyplot as plt

con = duckdb.connect("ecommerce.duckdb")

# data for charts
mro = con.execute("""
    SELECT month, total_orders, total_revenue
    FROM monthly_revenue_orders
    ORDER BY month
""").fetchdf()

top_products = con.execute("""
    SELECT p.product_name, SUM(s.total_price) AS total_revenue
    FROM stg_sales s
    JOIN stg_products p USING (product_id)
    GROUP BY p.product_name
    ORDER BY total_revenue DESC
    LIMIT 10
""").fetchdf()

clv_top = con.execute("""
    SELECT customer_id, total_orders, total_revenue
    FROM customer_lifetime_value
    ORDER BY total_revenue DESC
    LIMIT 10
""").fetchdf()

# layout: 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# (1) Monthly revenue (line)
axes[0,0].plot(mro["month"], mro["total_revenue"], marker="o")
axes[0,0].set_title("Monthly Revenue")
axes[0,0].set_xlabel("Month"); axes[0,0].set_ylabel("Total Revenue ($)")
for tick in axes[0,0].get_xticklabels(): tick.set_rotation(45)

# (2) Monthly orders (line)
axes[0,1].plot(mro["month"], mro["total_orders"], marker="o")
axes[0,1].set_title("Monthly Orders")
axes[0,1].set_xlabel("Month"); axes[0,1].set_ylabel("Total Orders")
for tick in axes[0,1].get_xticklabels(): tick.set_rotation(45)

# (3) Top products by revenue (horizontal bars)
axes[1,0].barh(top_products["product_name"], top_products["total_revenue"])
axes[1,0].invert_yaxis()
axes[1,0].set_title("Top 10 Products by Revenue")
axes[1,0].set_xlabel("Total Revenue ($)"); axes[1,0].set_ylabel("Product")

# (4) Small table: Top customers by revenue
axes[1,1].axis("off")
table = axes[1,1].table(
    cellText=clv_top.values,
    colLabels=clv_top.columns.tolist(),
    loc="center"
)
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.2)
axes[1,1].set_title("Top 10 Customers by Revenue", pad=10)

plt.tight_layout()
plt.savefig("dashboard.png", dpi=200)
plt.savefig("dashboard.pdf")
plt.close()
print("✅ Saved dashboard.png and dashboard.pdf")

