import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("expenses.xlsx")
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# Show first few rows
print("First 5 rows:")
print(df.head())

# Basic info
print("\nColumn names:")
print(df.columns)

# Total expense
total_expense = df["Amount"].sum()
print("\nTotal Expense:", total_expense)

# Category-wise expense
category_expense = df.groupby("Category")["Amount"].sum()
print("\nCategory-wise Expense:")
print(category_expense)
# Highest and lowest spending category
max_cat = category_expense.idxmax()
max_amt = category_expense.max()

min_cat = category_expense.idxmin()
min_amt = category_expense.min()

print(f"\nHighest spending category: {max_cat} -> {max_amt}")
print(f"Lowest spending category: {min_cat} -> {min_amt}")
# Step 5: Visualization
plt.figure(figsize=(8,5))
category_expense.plot(kind='bar', color='skyblue')
plt.title("Expenses by Category")
plt.xlabel("Category")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# Step 6: Save summary to CSV
summary_df = category_expense.reset_index()
summary_df.columns = ['Category', 'Amount']
summary_df.to_csv("category_summary.csv", index=False)
print("\nCategory summary saved to category_summary.csv")