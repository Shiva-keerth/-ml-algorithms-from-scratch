import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Uber Analytics", layout="wide")

df = pd.read_csv("uber.csv")

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dataset", "Overview", "Ride Analytics","Data Assistance"],
        icons=["table", "bar-chart", "graph-up","robot"],
        menu_icon="car-front",
        default_index=0
    )

# ---------------- DATASET PAGE ---------------- #

if selected == "Dataset":

    st.title("Dataset Explorer")

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isna().sum().sum())

    st.divider()

    # column selection
    selected_columns = st.multiselect(
        "Choose columns to display",
        df.columns,
        default=df.columns
    )

    filtered_df = df[selected_columns]

    # search dataset
    st.subheader("Search in Dataset")

    search_value = st.text_input("Search Any Value")

    if search_value:
        filtered_df = filtered_df[
            filtered_df.astype(str).apply(
                lambda row: row.str.contains(search_value, case=False).any(),
                axis=1
            )
        ]

    # column filter
    st.subheader("Column Filter")

    col1, col2 = st.columns(2)

    with col1:
        filter_column = st.selectbox("Select Column", filtered_df.columns)

    with col2:
        filter_value = st.selectbox(
            "Select Value",
            filtered_df[filter_column].dropna().unique()
        )

    if st.button("Apply Filter"):
        filtered_df = filtered_df[filtered_df[filter_column] == filter_value]

    st.divider()

    # row display
    st.subheader("Row display")

    rows = st.slider(
        "Number of row display",
        min_value=10,
        max_value=len(filtered_df),
        value=100
    )

    # dataset table
    st.subheader("Dataset Table")
    st.dataframe(filtered_df.head(rows), use_container_width=True)

    # show full dataset
    if st.checkbox("Show all dataset"):
        st.dataframe(df, use_container_width=True)

    st.divider()

    # columns statistics
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select Numeric Column", numeric_cols)
        st.write(filtered_df[selected_col].describe())

    st.divider()

    # download dataset
    st.subheader("Download dataset")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Dataset",
        csv,
        file_name="dataset.csv",
        mime="text/csv"
    )


# ---------------- OVERVIEW PAGE ---------------- #

if selected == "Overview":
    st.title("Uber Operation: Strategic Executive Overview")

    total_rides = len(df)

    completed_rides = df[df["Booking Status"] == "Completed"]
    total_revenue = completed_rides["Booking Value"].sum()

    avg_distance = completed_rides["Ride Distance"].mean()

    success_rate = (len(completed_rides) / total_rides * 100) if total_rides > 0 else 0

    avg_rating = completed_rides["Customer Rating"].dropna().mean()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        label="Gross Booking Value",
        value=f"{total_revenue:.0f}",
        delta="Target: 1000000"
    )

    kpi2.metric(
        label="Fulfillment Rate",
        value=f"{success_rate:.2f}%",
        delta="-2.4% vs Last Month",
        delta_color="red"
    )

    kpi3.metric(
        label="Avg Distance",
        value=f"{avg_distance:.2f} km"
    )

    kpi4.metric(
        label="Avg Rating",
        value=f"{avg_rating:.1f}/5.0"
    )

    st.divider()

    # Business unit performance
    st.subheader("Business Unit Performance Matrix")

    bu_metrics = df.groupby("Vehicle Type").agg(
        Total_Bookings=("Booking ID", "count"),
        Revenue_Generated=("Booking Value", "sum"),
        Avg_Distance=("Ride Distance", "mean"),
        Avg_Rating=("Customer Rating", "mean")
    )

    bu_metrics["Revenue Share %"] = (
        bu_metrics["Revenue_Generated"] / total_revenue * 100
        if total_revenue > 0 else 0
    )

    st.dataframe(
        bu_metrics.style.format({
            "Revenue_Generated": "{:.2f}",
            "Avg_Distance": "{:.2f}",
            "Avg_Rating": "{:.1f}"
        }).background_gradient(
            subset=["Revenue_Generated", "Revenue Share %"],
            cmap="winter_r"
        ),
        use_container_width=True
    )

    st.divider()

    # Operational efficiency
    col_eff, col_can = st.columns(2)

    with col_eff:
        st.subheader("Operational Efficiency")

        eff_df = df.groupby("Vehicle Type")[["Avg VTAT", "Avg CTAT"]].mean()
        st.write("Average Turn Around time")

        st.dataframe(
            eff_df.style
            .highlight_max(axis=0, color="#ffccff")
            .highlight_min(axis=0, color="#ccffcc"),
            use_container_width=True
        )

    # Cancellation Audit
    with col_can:
        st.subheader("Cancellation Audit")
        st.write("All Booking Percentage")

        status_count = df["Booking Status"].value_counts().to_frame(name="count")
        status_count["Share %"] = (status_count["count"] / total_rides * 100)

        st.dataframe(status_count, use_container_width=True)

    # Financial Deep Dive
    st.subheader("Financial Deep Dive")

    pay_col, reason_col = st.columns([4, 6])

    with pay_col:
        st.markdown("**Payment Method Preference**")

        pay_summary = (
            completed_rides["Payment Method"]
            .value_counts(normalize=True) * 100
        )

        st.dataframe(
            pay_summary.rename("Usage %"),
            use_container_width=True
        )

    with reason_col:
        st.markdown("**Primary Cancellation Triggers**")

        cust_reasons = (
            df["Reason for cancelling by Customer"]
            .dropna()
            .value_counts()
            .head(3)
        )

        drv_reasons = (
            df["Driver Cancellation Reason"]
            .dropna()
            .value_counts()
            .head(3)
        )

        cust_reasons.index = "Customer: " + cust_reasons.index
        drv_reasons.index = "Driver: " + drv_reasons.index

        reason_df = pd.concat([cust_reasons, drv_reasons]).to_frame(name="Incident Count")

        st.dataframe(reason_df)

    # Data Quality Audit
    with st.expander("Data Quality and Audit"):

        audit1, audit2 = st.columns(2)

        audit1.write(f"**Duplicate Records:** {df.duplicated().sum()}")
        audit2.write(f"**Missing Values:** {df['Booking Value'].isna().sum()}")

        st.info("Missing Booking Values are expected for cancelled or no driver found")

        st.success("Executive Overview Generated From Operational Dataset")

if selected == "Ride Analytics":
    st.title("Aadvance Ride Analyics Dahsboard")

    st.divider()

    st.subheader("Booking Status Distribution")
    status_counts = df['Booking Status'].value_counts().reset_index()
    fig = px.pie(status_counts, names='Booking Status', values='count',
                 title='Overall Booking Status Distribution', hole=0.3)
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    st.subheader("Vehicle Type Popularity")

    vehicle_counts = df['Vehicle Type'].value_counts().reset_index()
    fig = px.bar(vehicle_counts, x='Vehicle Type', y='count',
                 title='Total Bookings by Vehicle Type', color='Vehicle Type')
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    st.subheader("Total Revenue by Vehicle Type")

    revenue_by_vehicle = df.groupby('Vehicle Type')['Booking Value'].sum().reset_index()
    fig = px.bar(revenue_by_vehicle.sort_values(by='Booking Value', ascending=False),
                 x='Vehicle Type', y='Booking Value', title='Total Revenue per Vehicle Category')
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    st.subheader("Daily Booking Volume Trend")

    df['Date'] = pd.to_datetime(df['Date'])
    daily_bookings = df.groupby('Date').size().reset_index(name='Booking Count')
    fig = px.line(daily_bookings, x='Date', y='Booking Count',
                  title='Daily Booking Trends', markers=True)
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    st.subheader("Ride Distance vs. Booking Value")



    st.subheader("Average Vehicle Arrival Time (VTAT) by Category")

    avg_vtat = df.groupby('Vehicle Type')['Avg VTAT'].mean().reset_index()
    fig = px.bar(avg_vtat.sort_values(by='Avg VTAT'), x='Vehicle Type', y='Avg VTAT',
                 title='Average Vehicle Arrival Time (VTAT) in Minutes')
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    st.subheader("Customer Cancellation Reasons")

    cust_cancel = df['Reason for cancelling by Customer'].value_counts().reset_index()
    fig = px.bar(cust_cancel, x='count', y='Reason for cancelling by Customer',
                 orientation='h', title='Top Reasons for Customer Cancellations')
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    st.subheader("Driver Rating Distribution")

    fig = px.histogram(df, x='Driver Ratings', nbins=10,
                       title='Distribution of Driver Ratings', marginal="box")
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    st.subheader("Payment Method Preference")

    payment_counts = df['Payment Method'].value_counts().reset_index()
    fig = px.pie(payment_counts, names='Payment Method', values='count',
                 title='Preferred Payment Methods')
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    st.subheader("Ride Distance Distribution")

    fig = px.histogram(df, x='Ride Distance', title='Distribution of Ride Distances',
                       color_discrete_sequence=['indianred'])
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    completed = df[df["Booking Status"]=="Completed"]

    # sunbust

    st.subheader("Revenue Hierarchy")



    fig1 = px.sunburst(
        completed,
        path=["Vehicle Type", "Payment Method"],
        values="Booking Value",
        color="Booking Value",
        color_continuous_scale="Turbo"
    )

    fig1.update_layout(height=500)

    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # tree map

    st.subheader("Revenue Distribution")

    fig2 = px.treemap(
        completed,
        path=["Vehicle Type", "Payment Method"],
        values="Booking Value",
        color="Booking Value",
        color_continuous_scale="Blues"
    )

    fig2.update_layout(
        margin=dict(t=20, l=0, r=0, b=0),
        height=420
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # box chart

    st.subheader("Customer Rating Spread")

    fig3 = px.box(
        completed,
        x="Vehicle Type",
        y="Customer Rating",
        color="Vehicle Type"
    )

    fig3.update_layout(
        showlegend=False,
        height=420
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.divider()

    # sankey

    st.subheader("Ride Flow Analysis")

    flow = df.groupby(["Vehicle Type", "Booking Status"]).size().reset_index(name="count")

    source_labels = flow["Vehicle Type"].unique().tolist()
    target_labels = flow["Booking Status"].unique().tolist()

    labels = source_labels + target_labels

    source = flow["Vehicle Type"].apply(lambda x: labels.index(x)).tolist()
    target = flow["Booking Status"].apply(lambda x: labels.index(x)).tolist()
    value = flow["count"].tolist()

    import plotly.graph_objects as go

    fig4 = go.Figure(
        data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            )
        )]
    )

    fig4.update_layout(height=500)

    st.plotly_chart(fig4, use_container_width=True)

if selected == "Data Assistance":
    st.title("Data Assistant")
    st.divider()

    st.write("Ask Question About The Dataset And Get Visual Analytics")
    user_question = st.text_input("Ask Your Question")

    if user_question:
        q = user_question.lower()

        completed = df[df["Booking Status"]=="Completed"]

        if "total rides" in q:
            total = len(df)

            st.success(f"Total Rides In Dataset: {total}")

            status = df["Booking Status"].value_counts()

            fig = px.bar(x=status.index,y=status.values,
                         labels={"x":"Booking Status","y":"Ride count"},
                         title="Ride Distribution")
            st.plotly_chart(fig,use_container_width=True)

        elif "revenue" in q:
            revenue = completed.groupby("Vehicle Type")["Booking Value"].sum()
            st.success(f"Total Revenue:{revenue.sum():,.2f}")
            fig = px.bar(x=revenue.index, y=revenue.values,
                         title="Revenue Generated",
                         labels={"x":"Vehicle Type","y":"Revenue"})

            st.plotly_chart(fig,use_container_width=True)

        elif "vehicle" in q:

            vehicle = df["Vehicle Type"].value_counts()
            st.success(f"Most Used Vehicle Type: {vehicle.idxmax()}")

            fig = px.pie(names=vehicle.index,values=vehicle.values,
                         title="Vehicle Usage")
            st.plotly_chart(fig,use_container_width=True)

        elif "payment" in q:

            payment = completed["Payment Method"].value_counts()

            fig = px.pie(names=payment.index,
                         values=payment.values,
                         title="Payment Option Usage")

            st.plotly_chart(fig,use_container_width=True)
            st.dataframe(payment)

        elif "cancel" in q:
            cancel = df["Booking Status"].value_counts()

            fig = px.bar(x=cancel.index,
                         y=cancel.values,
                         title = "Ride Status",
                         labels={"x":"Status","y":"Ride count"})
            st.plotly_chart(fig,use_container_width=True)

        elif "rating" in q:
            fig = px.histogram(completed,x="Customer Rating",
                               nbins=10,title="Customer Rating")
            st.plotly_chart(fig,use_container_width=True)

            st.success(f"Average Rating:{completed["Customer Rating"].mean():.2f}")

        elif "distance" in q:
            fig = px.scatter(completed,x="Ride Distance",y="Booking Value",
                             color="Vehicle Type",title="Ride Distance vs Booking Value")

            st.plotly_chart(fig,use_container_width=True)
            st.success(f"Average Distance: {completed["Ride Distance"].mean():.2f}km")

        else:
            st.warning("Question Not Recognized. Try Asking About Revenue,Vehicle,Pyment,Cancellation,Rating Or Diastance")