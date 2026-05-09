import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bank Transaction Dashboard",layout="wide")

st.title("Bank Transaction Dashboard")

def load_data():
    df= pd.read_csv("bank_data.csv")
    df["Date"]= pd.to_datetime(df["Date"])
    return df

df= load_data()

# sidebar

st.sidebar.header("Filter Data")

# data filter

start_date = st.sidebar.date_input("Start Date",df["Date"].min())
end_date = st.sidebar.date_input("End Date",df["Date"].max())

# transaction type

t_type = st.sidebar.multiselect("select transaction type",df["Transaction_Type"].unique())

# category type

category = st.sidebar.multiselect("Select Category",df["Category"].unique())

# payment mode

p_mode = st.sidebar.multiselect("Select Payment Mode",df["Payment_Mode"].unique())

# city

city = st.sidebar.multiselect("Select City",df["City"].unique())

# top N Filter

top_n = st.sidebar.slider("Top N Products",1,10,5)

# apply filter

filtered_df = df[(df["Date"]>=pd.to_datetime(start_date)) &
                 (df["Date"]<=pd.to_datetime(end_date)) &
                 (df["Transaction_Type"].isin(t_type)) &
                 (df["Category"].isin(category)) &
                 (df["Payment_Mode"].isin(p_mode)) &
                 (df["City"].isin(city))]

# KPI section

total_amount = filtered_df["Amount"].sum()
total_balance_after_transaction = filtered_df["Balance_After_Transaction"].sum()
total_credit = (filtered_df["Transaction_Type"]=="Credit").sum()
total_debit = (filtered_df["Transaction_Type"]=="Debit").sum()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Amount",f"{total_amount}")

col2.metric("Total Balance After Transaction",f"{total_balance_after_transaction}")

col3.metric("Total Credit",f"{total_credit}")

col4.metric("Total Debit",f"{total_debit}")


st.markdown("-----")

# chart selection

# CITY VS AMOUNT

col4,col5 = st.columns(2)

city_amount = filtered_df.groupby("City")["Amount"].sum().reset_index()

fig_bar = px.bar(city_amount,
                 x="City",
                 y="Amount",color="City",title="City Wise Sales")

col4.plotly_chart(fig_bar,use_container_width=True)

# top N product

# CATEGORY VS AMOUNT

category_amount = filtered_df.groupby("Category")["Amount"].sum().reset_index()
category_amount = category_amount.sort_values(by="Amount",ascending=False).head(top_n)
fig_top = px.bar(category_amount,
                 x="Category",
                 y="Amount",
                 color="Category",
                 title=f"Top {top_n} Category")

col5.plotly_chart(fig_top,use_container_width=True)

# LINE CHART

# date VS AMOUNT (TREND)

date_amount = filtered_df.groupby("Date")["Amount"].sum().reset_index()

fig_line = px.line(
    date_amount,
    x="Date",
    y="Amount",
    title="Date Wise Amount"
)

st.plotly_chart(fig_line,use_container_width=True)

# CATEGORY DISTRIBUTION (PIE)

category_data = filtered_df.groupby("Category")["Amount"].sum().reset_index()

fig_pie = px.pie(
    category_data,
    names="Category",
    values="Amount",
    title="Category Distribution"
)

st.plotly_chart(fig_pie,use_container_width=True)

# TRANSACTION TYPE

# DONUT

# Transaction Type Donut Chart

transaction_data = filtered_df.groupby("Transaction_Type")["Amount"].sum().reset_index()

fig_donut = px.pie(
    transaction_data,
    names="Transaction_Type",
    values="Amount",
    hole=0.4,
    title="Transaction Type Distribution"
)

st.plotly_chart(fig_donut, use_container_width=True)

# AMOUNT VS BALANCE AFTER TRANSACTION

# SCATTER

fig_scatter = px.scatter(
    filtered_df,
    x="Amount",
    y="Balance_After_Transaction",
    color="Transaction_Type",
    title="Amount vs Balance"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# AMOUNT DISTRIBUTION

# HISTOGRAM

fig_hist = px.histogram(
    filtered_df,
    x="Amount",
    nbins=20,
    title="Transaction Amount Distribution"
)

st.plotly_chart(fig_hist, use_container_width=True)