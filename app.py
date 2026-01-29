import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Spenswise Analyzer", layout="centered")

st.title("💰 SpendWise Analyzer")
st.write("Smart expense tracking made simple")

DATA_FILE = "expenses.csv"

# ---------- Load or Create Data ----------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Month", "Note"])

# ---------- Add New Expense ----------
st.header("➕ Add Today’s Expense")

expense_date = st.date_input("Date", date.today())
category = st.selectbox(
    "Category",
    ["Food", "Travel", "Books", "Rent", "Entertainment", "Other"]
)
amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
note = st.text_input("Note (optional)")

if st.button("Save Expense"):
    new_row = {
        "Date": expense_date.strftime("%Y-%m-%d"),  # STRING (important)
        "Category": category,
        "Amount": amount,
        "Month": expense_date.strftime("%Y-%m"),
        "Note": note if note else "-"
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    st.success("✅ Expense saved successfully!")
    st.rerun()   # FORCE refresh

# ---------- Show All Expenses ----------
st.header("📋 All Expenses")

if df.empty:
    st.info("No expenses added yet.")
else:
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df = df.sort_values(by="Date", ascending=False)

    st.dataframe(df, width="stretch")


# ================================
# MONTHLY TOTAL SPENDING
# ================================

st.subheader("💰 Total Monthly Spending")

monthly_total = (
    df.groupby("Month")["Amount"]
    .sum()
    .reset_index()
)

for _, row in monthly_total.iterrows():
    st.metric(
        label=f"Month: {row['Month']}",
        value=f"₹ {row['Amount']}"
    )


# ================================
# MONTHLY SUMMARY CHART
# ================================

st.header("📊 Monthly Expense Summary")

if df.empty:
    st.info("No data to show")
else:
    monthly_summary = df.groupby("Month")["Amount"].sum().reset_index()
    st.bar_chart(monthly_summary.set_index("Month"))
