import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
# App Title 

# Upload File 
st.title("Student Expense Analyzer")
st.write("App is running successfully ")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show first 5 rows
    st.write("### Sample Data")
    st.dataframe(df.head())

    # Total Expense
    total = df['Amount'].sum()
    st.write(f"**Total Expense:** {total}")

    # Category-wise Expense
    cat_exp = df.groupby("Category")['Amount'].sum()
    st.write("### Expense by Category")
    st.dataframe(cat_exp)

    # Highest & Lowest Category
    max_cat = cat_exp.idxmax()
    min_cat = cat_exp.idxmin()
    st.write(f"**Highest Spending Category:** {max_cat} → {cat_exp[max_cat]}")
    st.write(f"**Lowest Spending Category:** {min_cat} → {cat_exp[min_cat]}")

    # Bar Chart
    st.write("### Bar Chart of Expenses by Category")
    plt.figure(figsize=(8,5))
    cat_exp.plot(kind='bar', color='skyblue')
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # Save Summary
    summary = cat_exp.reset_index()
    summary.columns = ['Category', 'Amount']
    summary.to_csv("category_summary.csv", index=False)
    st.write("✅ Summary saved as category_summary.csv")
