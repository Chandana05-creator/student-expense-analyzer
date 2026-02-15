import streamlit as st
import pandas as pd
import os
from datetime import date
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="SpendWise Analyzer", layout="centered")

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<h1 style='color:blue;'>💰 SpendWise Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:green;'>Smart expense tracking made simple!</h3>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# USER NAME (store permanently)
# -----------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if st.session_state.user_name == "":
    name_input = st.text_input("👤 Enter your name")
    if name_input:
        st.session_state.user_name = name_input
        st.success(f"Welcome {name_input} 👋")
        st.rerun()
else:
    st.write(f"👤 Logged in as: {st.session_state.user_name}")

user_name = st.session_state.user_name

if user_name:
    DATA_FILE = f"{user_name.lower().replace(' ', '_')}_expenses.csv"
else:
    DATA_FILE = None

# -----------------------------
# LOAD OR CREATE DATA
# -----------------------------
if DATA_FILE:
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Month", "Note"])
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Month", "Note"])

# -----------------------------
# ADD NEW EXPENSE
# -----------------------------
st.header("➕ Add Today’s Expense")

expense_date = st.date_input("Date", date.today())
category = st.selectbox(
    "Category",
    ["Food", "Snacks", "Travel", "Books", "Rent", "Entertainment",
     "Home Appliances", "Health", "Grocery","electric bill","water bill","petroleum","Other"]
)
amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
note = st.text_input("Note (optional)")

if st.button("Save Expense"):
    if not user_name:
        st.error("❌ Please enter your name first")
    else:
        new_row = {
            "Date": expense_date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
            "Month": expense_date.strftime("%Y-%m"),
            "Note": note if note else "-"
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Expense saved successfully!")
        st.rerun()

# -----------------------------
# SHOW ALL EXPENSES
# -----------------------------
st.header("📋 All Expenses")

if df.empty:
    st.info("No expenses added yet.")
else:
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df = df.sort_values(by="Date", ascending=False)
    st.dataframe(df, width="stretch")

# -----------------------------
# MONTHLY TOTAL SPENDING
# -----------------------------
st.subheader("💰 Total Monthly Spending")

if not df.empty:
    monthly_total = df.groupby("Month")["Amount"].sum().reset_index()
    for _, row in monthly_total.iterrows():
        st.metric(
            label=f"Month: {row['Month']}",
            value=f"₹ {row['Amount']}"
        )

# -----------------------------
# MONTHLY SUMMARY CHART
# -----------------------------
st.header("📊 Monthly Expense Summary")

if df.empty:
    st.info("No data to show")
else:
    monthly_summary = df.groupby("Month")["Amount"].sum().reset_index()
    st.bar_chart(monthly_summary.set_index("Month"))

# -----------------------------
# EXPENSE BY CATEGORY
# -----------------------------
if not df.empty:
    st.header("📈 Expense by Category")

    category_sum = df.groupby("Category")["Amount"].sum().reset_index()
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(category_sum)

    with col2:
        fig, ax = plt.subplots()
        ax.pie(
            category_sum["Amount"],
            labels=category_sum["Category"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)

    # Top category
    top_category = category_sum.loc[category_sum["Amount"].idxmax()]
    st.markdown(
        f"🔥 **Top Expense:** {top_category['Category']} – ₹{top_category['Amount']}"
    )

# -----------------------------
# FOOTER TIP
# -----------------------------
st.markdown(
    """
    💡 **Tip:**  
    Track expenses daily and reduce spending in your top category to save more!
    """
)
