import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Student Expense Analyzer", layout="centered")

st.title("📊 Student Expense Analyzer")
st.write("Analyze your expenses easily — upload CSV or enter manually.")
# SESSION STATE INITIALIZATION
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=["Date", "Category", "Amount"]
    )
# INPUT METHOD SELECTION
option = st.radio(
    "How would you like to add expenses?",
    ("Upload CSV", "Enter Manually")
)
# OPTION 1: CSV UPLOAD
if option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            df.columns = ["Date", "Category", "Amount"]
            st.session_state.expenses = df
            st.success("CSV uploaded successfully!")
        except:
            st.error("CSV format should be: Date, Category, Amount")
# OPTION 2: MANUAL ENTRY
if option == "Enter Manually":
    st.subheader("➕ Add Expense")

    exp_date = st.date_input("Date", date.today())
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Rent", "Education", "Shopping", "Other"]
    )
    amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)

    if st.button("Add Expense"):
        new_data = {
            "Date": exp_date,
            "Category": category,
            "Amount": amount
        }

        st.session_state.expenses = pd.concat(
            [st.session_state.expenses, pd.DataFrame([new_data])],
            ignore_index=True
        )

        st.success("Expense added successfully!")
# DATA DISPLAY & ANALYSIS
if not st.session_state.expenses.empty:
    df = st.session_state.expenses

    st.subheader("📋 Expense Records")
    st.dataframe(df)

    st.subheader("📈 Category-wise Expense Summary")
    summary = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    summary.plot(kind="bar", ax=ax)
    ax.set_ylabel("Amount (₹)")
    ax.set_xlabel("Category")
    st.pyplot(fig)

    st.subheader("🥧 Expense Distribution")
    fig2, ax2 = plt.subplots()
    ax2.pie(summary, labels=summary.index, autopct="%1.1f%%")
    st.pyplot(fig2)

    st.download_button(
        "⬇️ Download Expenses as CSV",
        df.to_csv(index=False),
        "expenses.csv",
        "text/csv"
    )

else:
    st.info("No expense data available. Add expenses to see analysis.")
