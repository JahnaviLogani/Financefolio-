import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, save_expense

st.set_page_config(
    page_title="FinanceFolio",
    page_icon="💰",
    layout="wide"
)

st.title("💰 FinanceFolio")
st.subheader("Personal Expense Tracker")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Add Expense",
        "View Expenses",
        "Reports"
    ]
)

##############################################################

if menu=="Add Expense":

    st.header("Add New Expense")

    date = st.date_input("Date")

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Education",
            "Health",
            "Other"
        ]
    )

    description = st.text_input("Description")

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    if st.button("Save Expense"):

        save_expense(date,category,description,amount)

        st.success("Expense Added Successfully!")

##############################################################

elif menu=="View Expenses":

    st.header("All Expenses")

    df = load_data()

    if len(df)==0:
        st.warning("No Expenses Found")
    else:

        search = st.text_input("Search")

        if search!="":
            df=df[df["Description"].str.contains(search,case=False)]

        st.dataframe(df,use_container_width=True)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "expenses.csv",
            "text/csv"
        )

##############################################################

elif menu=="Dashboard":

    st.header("Dashboard")

    df=load_data()

    if len(df)==0:

        st.warning("No Data Available")

    else:

        total=df["Amount"].sum()

        avg=df["Amount"].mean()

        count=len(df)

        c1,c2,c3=st.columns(3)

        c1.metric("Total Expense",f"₹ {total:.2f}")

        c2.metric("Average Expense",f"₹ {avg:.2f}")

        c3.metric("Transactions",count)

        st.divider()

        pie=px.pie(
            df,
            names="Category",
            values="Amount",
            title="Expenses by Category"
        )

        st.plotly_chart(pie,use_container_width=True)

##############################################################

elif menu=="Reports":

    st.header("Expense Report")

    df=load_data()

    if len(df)==0:

        st.warning("No Data Available")

    else:

        df["Date"]=pd.to_datetime(df["Date"])

        df["Month"]=df["Date"].dt.strftime("%B")

        report=df.groupby("Month")["Amount"].sum().reset_index()

        st.dataframe(report,use_container_width=True)

        bar=px.bar(
            report,
            x="Month",
            y="Amount",
            color="Amount",
            title="Monthly Expenses"
        )

        st.plotly_chart(bar,use_container_width=True)

        category=df.groupby("Category")["Amount"].sum().reset_index()

        st.subheader("Category Wise Report")

        st.dataframe(category)

        fig=px.bar(
            category,
            x="Category",
            y="Amount",
            color="Category"
        )

        st.plotly_chart(fig,use_container_width=True)