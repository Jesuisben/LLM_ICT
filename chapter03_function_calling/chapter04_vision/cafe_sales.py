import matplotlib.pyplot as plt

image_path = '../images/'
# -----------------------------
# 1. 데이터 정의
# -----------------------------
products = ["Americano", "Latte", "Cappuccino", "Mocha", "Cold Brew"]

sales_2025 = [120, 150, 400, 110, 130]
sales_2026 = [140, 170, 105, 125, 160]

# y축 최대값 (비교용으로 고정)
y_max = 200

# -----------------------------
# 2. 2025년 매출 그래프
# -----------------------------
plt.figure(figsize=(8, 5))
plt.bar(products, sales_2025)
plt.ylim(0, y_max)
plt.title("Cafe Product Sales - 2025", size=20)
plt.xlabel("Product", size=15)
plt.ylabel("Sales (Unit: Million KRW)", size=15)
plt.tight_layout()
plt.savefig(image_path + "cafe_sales_2025.png")
plt.close()

# -----------------------------
# 3. 2026년 매출 그래프
# -----------------------------
plt.figure(figsize=(8, 5))
plt.bar(products, sales_2026)
plt.ylim(0, y_max)
plt.title("Cafe Product Sales - 2026", size=20)
plt.xlabel("Product", size=15)
plt.ylabel("Sales (Unit: Million KRW)", size=15)
plt.tight_layout()
plt.savefig(image_path + "cafe_sales_2026.png")
plt.close()

print("PNG files saved: cafe_sales_2025.png, cafe_sales_2026.png")