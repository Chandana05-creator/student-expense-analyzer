import streamlit as st
import pandas as pd
import os
DATA_FILE = "spendwise_data.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
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
# ✅ ADD THIS LINE HERE
note = st.text_input("Note (optional)")

if st.button("Save Expense"):
     new_row = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Note": note
    }

     df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
     df.to_csv(DATA_FILE, index=False)
     st.success("Expense added successfully!")

# ---------- Show Daily Data ----------
st.header("📋 All Expenses")
st.dataframe(df)

# ---------- Monthly Summary ----------
st.header("📊 Monthly Expense Summary")
df["Date"] = pd.to_datetime(df["Date"])
monthly_total = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum()

st.bar_chart(monthly_total)

if not df.empty:
    monthly_summary = df.groupby("Month")["Amount"].sum().reset_index()

    st.bar_chart(monthly_summary.set_index("Month"))

    st.write("### Monthly Totals")
    st.dataframe(monthly_summary)
else:
    st.info("No expenses added yet.")
