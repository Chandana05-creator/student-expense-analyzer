import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="SpendWise Analyzer", layout="centered")

# -----------------------------
# GOOGLE SHEETS CONNECTION
# -----------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)
client = gspread.authorize(creds)


# 👉 Replace with your Google Sheet name
SHEET_NAME = "SpendWiseData"

try:
    sheet = client.open("Student Expense Data").sheet1
except:
    sheet = client.create(SHEET_NAME).sheet1
    sheet.append_row(["User", "Date", "Category", "Amount", "Month", "Note"])

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<h1 style='color:blue;'>💰 SpendWise Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:green;'>Smart expense tracking made simple!</h3>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# USER LOGIN (ONE TIME)
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

# -----------------------------
# LOAD DATA FROM GOOGLE SHEETS
# -----------------------------
data = sheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty:
    df = df[df["User"] == user_name]

# -----------------------------
# ADD EXPENSE
# -----------------------------
st.header("➕ Add Today’s Expense")

expense_date = st.date_input("Date", date.today())
category = st.selectbox(
    "Category",
    ["Food", "Snacks", "Travel", "Books", "Rent", "Entertainment",
     "Home Appliances", "Health", "Grocery",
     "electric bill", "water bill", "petroleum", "Other"]
)
amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
note = st.text_input("Note (optional)")

if st.button("Save Expense"):
    if not user_name:
        st.error("❌ Please enter your name first")
    else:
        sheet.append_row([
            user_name,
            expense_date.strftime("%Y-%m-%d"),
            category,
            amount,
            expense_date.strftime("%Y-%m"),
            note if note else "-"
        ])
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
# MONTHLY TOTAL
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
# MONTHLY CHART
# -----------------------------
st.header("📊 Monthly Expense Summary")

if not df.empty:
    monthly_summary = df.groupby("Month")["Amount"].sum().reset_index()
    st.bar_chart(monthly_summary.set_index("Month"))
else:
    st.info("No data to show")

# -----------------------------
# CATEGORY ANALYSIS
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

    top_category = category_sum.loc[category_sum["Amount"].idxmax()]
    st.markdown(
        f"🔥 **Top Expense:** {top_category['Category']} – ₹{top_category['Amount']}"
    )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown(
    """
    💡 **Tip:**  
    Track expenses daily and reduce spending in your top category to save more!
    """
)
