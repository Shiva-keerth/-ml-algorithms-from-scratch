import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard",layout="wide")

st.title("Sales Dashboard")

def load_data():
    df = pd.read_csv("sales.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# sidebar

st.sidebar.header("Filter Data")

# data filter

start_date = st.sidebar.date_input("Start Date",df["Date"].min())
end_date = st.sidebar.date_input("End Date",df["Date"].max())

# region filter

region = st.sidebar.multiselect("Select Region",df["Region"].unique())

# product filter

product = st.sidebar.multiselect("Select Product",df["Product"].unique())

# top N filter

top_n = st.sidebar.slider("Top N Products",1,10,5)

# Apply Filter

filtered_df = df[(df["Date"]>=pd.to_datetime(start_date)) &
                 (df["Date"]<=pd.to_datetime(end_date)) &
                 (df["Region"].isin(region)) &
                 (df["Product"].isin(product))]

# KPI section

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
avg_sales = filtered_df["Sales"].mean()

# previous period comparison

previous_df = df[df["Date"] < pd.to_datetime(start_date)]
previous_sales = previous_df["Sales"].sum()

growth = 0

if previous_sales > 0:
    growth = ((total_sales-previous_sales)/previous_sales)*100

col1,col2,col3 = st.columns(3)

col1.metric("Total Sales",f"{total_sales}", f"{round(growth,2)}%")

col2.metric("Total Profit",f"{total_profit}")

col3.metric("Average Sales",f"{round(avg_sales,2)}")

st.markdown("---")

# chart selection

col4,col5 = st.columns(2)

sales_region = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig_bar = px.bar(sales_region,
                 x="Region",
                 y="Sales",color="Region",title="Sales By Region")

col4.plotly_chart(fig_bar,use_container_width=True)

# top N product

sales_product = filtered_df.groupby("Product")["Sales"].sum().reset_index()
sales_product = sales_product.sort_values(by="Sales",ascending=False).head(top_n)

fig_top = px.bar(sales_product,
                 x = "Product",y="Sales",color="Product",
                 title=f"Top {top_n} products by sales")
col5.plotly_chart(fig_top,use_container_width = True)

# sales trendline

fig_line = px.line(filtered_df, x="Date", y="Sales", color="Region", markers=True,
                   title="Sales Trend Over Time")

st.plotly_chart(fig_line,use_container_width=True)


# PIE CHART

profit_product = filtered_df.groupby("Product")["Profit"].sum().reset_index()

fig_pie = px.pie(profit_product, names="Product", values="Profit", hole=0.4, title="Profit Distribution")

st.plotly_chart(fig_pie,use_container_width=True)

st.markdown("### Download Filtered File")

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV",csv,"Filtered_sales_data.csv","text/csv")