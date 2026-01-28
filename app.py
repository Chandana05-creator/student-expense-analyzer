import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Student Expense Analyzer", layout="centered")

st.title("SpendWise – Smart Expense Tracker")
st.write("Track daily expenses & view monthly insights")

DATA_FILE = "expenses.csv"

# ---------- Load or Create Data ----------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Month"])

# ---------- Add New Expense ----------
st.header("➕ Add Today’s Expense")

expense_date = st.date_input("Date", date.today())
category = st.selectbox("category",
     [
        "Food",
        "Snacks",
        "Travel",
        "Books",
        "Home Appliances",
        "Rent",
        "Entertainment",
        "Mobile / Internet",
        "Medical",
        "Education",
        "Clothing",
        "Other"
    ]
)

amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)

if st.button("Save Expense"):
    month = expense_date.strftime("%Y-%m")

    new_row = {
        "Date": expense_date,
        "Category": category,
        "Amount": amount,
        "Month": month
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    st.success("✅ Expense saved successfully!")

# ---------- Show Daily Data ----------
st.header("📋 All Expenses")
st.dataframe(df)

# ---------- Monthly Summary ----------
st.header("📊 Monthly Expense Summary")

if not df.empty:
    monthly_summary = df.groupby("Month")["Amount"].sum().reset_index()

    st.bar_chart(monthly_summary.set_index("Month"))

    st.write("### Monthly Totals")
    st.dataframe(monthly_summary)
else:
    st.info("No expenses added yet.")
