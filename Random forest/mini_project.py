import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from streamlit_option_menu import option_menu
import datetime as dt
import streamlit as st
with st.sidebar:
    selected = option_menu(
        "RF_Mini_Project",
        ["Dataset", "Charts"],
        icons=["table", "bar-chart"],
        menu_icon="cast",
        orientation="vertical",
        default_index=0
    )

if selected == "Dataset":
    df = pd.read_csv("data - data.csv.csv")
    st.write(df)

    le_city = LabelEncoder()
    df["city"] = le_city.fit_transform(df["city"])

    x = df[["bedrooms","bathrooms","sqft_living","sqft_lot","floors","view","condition",
            "sqft_above","sqft_basement","yr_built","yr_renovated","city"]]
    y = df["price"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    model = RandomForestRegressor(n_estimators=500, random_state=42)
    model.fit(x_train, y_train)

    prediction = model.predict(x_test)

    # st.subheader("Predicted Prices (sample)")
    # st.write(prediction[:1])
    #
    # st.subheader("R2 Score")
    # st.write(r2_score(y_test, prediction))
    #
    # st.subheader("MAE")
    # st.write(mean_absolute_error(y_test, prediction))

    data1 = st.number_input("Enter the value1")
    data2 = st.number_input("Enter the value2")
    data3 = st.number_input("Enter the value3")
    data4 = st.number_input("Enter the value4")
    data5 = st.number_input("Enter the value5")
    data6 = st.number_input("Enter the value6")
    data7 = st.number_input("Enter the value7")
    data8 = st.number_input("Enter the value8")
    data9 = st.number_input("Enter the value9")
    data10 = st.number_input("Enter the value10")
    data11 = st.number_input("Enter the value11")
    data12 = st.number_input("Enter the value12")
    if st.button("Predict (Random forest)"):
        newdata = [[data1, data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12]]
        newprediction = model.predict(newdata)
        st.subheader("Predicted Value")
        st.write(newprediction)

if selected == "Charts":
    st.sidebar.title("Charts")

    df = pd.read_csv("data - data.csv.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    st.sidebar.title("Charts Menu")
    mode = st.sidebar.radio("Select Mode", ["Charts (Predefined)", "Custom Chart Builder"])

    # =========================
    # 1) PREDEFINED CHARTS
    # =========================
    if mode == "Charts (Predefined)":
        chart = st.sidebar.selectbox(
            "Select Chart",
            [
                "Bedrooms Count",
                "Price vs Sqft Living",
                "Avg Price by Bedrooms",
                "Monthly Avg Price Trend",
                "Top 10 Cities by Avg Price"
            ]
        )

        if chart == "Bedrooms Count":
            st.subheader("Bedrooms Count")
            counts = df["bedrooms"].value_counts().sort_index()

            fig, ax = plt.subplots()
            ax.bar(counts.index.astype(str), counts.values)
            ax.set_xlabel("Bedrooms")
            ax.set_ylabel("No. of Houses")
            st.pyplot(fig)

        elif chart == "Price vs Sqft Living":
            st.subheader("Price vs Sqft Living")

            fig, ax = plt.subplots()
            ax.scatter(df["sqft_living"], df["price"], alpha=0.5)
            ax.set_xlabel("Sqft Living")
            ax.set_ylabel("Price")
            st.pyplot(fig)

        elif chart == "Avg Price by Bedrooms":
            st.subheader("Average Price by Bedrooms")
            grp = df.groupby("bedrooms")["price"].mean().sort_index()

            fig, ax = plt.subplots()
            ax.bar(grp.index.astype(str), grp.values)
            ax.set_xlabel("Bedrooms")
            ax.set_ylabel("Average Price")
            st.pyplot(fig)

        elif chart == "Monthly Avg Price Trend":
            st.subheader("Monthly Average Price Trend")

            if "date" not in df.columns or df["date"].isna().all():
                st.warning("Date column not available / not in datetime format.")
            else:
                monthly = df.groupby(df["date"].dt.to_period("M"))["price"].mean()
                monthly.index = monthly.index.astype(str)

                fig, ax = plt.subplots()
                ax.plot(monthly.index, monthly.values)
                ax.set_xlabel("Month")
                ax.set_ylabel("Average Price")
                ax.tick_params(axis="x", rotation=45)
                st.pyplot(fig)

        elif chart == "Top 10 Cities by Avg Price":
            st.subheader("Top 10 Cities by Average Price")

            top_cities = (
                df.groupby("city")["price"]
                .mean()
                .sort_values(ascending=False)
                .head(10)
            )

            fig, ax = plt.subplots()
            ax.barh(top_cities.index.astype(str), top_cities.values)
            ax.set_xlabel("Average Price")
            ax.set_ylabel("City")
            st.pyplot(fig)

    # =========================
    # 2) CUSTOM CHART BUILDER
    # =========================
    else:
        st.sidebar.header("Custom Chart Builder")

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(include="object").columns.tolist()

        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            ["Bar", "Barh", "Line", "Scatter", "Histogram"]
        )

        fig, ax = plt.subplots()

        if chart_type in ["Bar", "Barh"]:
            x_col = st.sidebar.selectbox("Select Category (X)", categorical_cols)
            y_col = st.sidebar.selectbox("Select Numeric (Y)", numeric_cols)

            agg = st.sidebar.selectbox("Aggregation", ["mean", "sum", "count"])
            top_n = st.sidebar.slider("Show Top N", 5, 30, 10)

            if agg == "mean":
                grouped = df.groupby(x_col)[y_col].mean().sort_values(ascending=False).head(top_n)
            elif agg == "sum":
                grouped = df.groupby(x_col)[y_col].sum().sort_values(ascending=False).head(top_n)
            else:
                grouped = df.groupby(x_col)[y_col].count().sort_values(ascending=False).head(top_n)

            if chart_type == "Bar":
                ax.bar(grouped.index.astype(str), grouped.values)
                # ax.tick_params(axis="x", rotation=45)
            else:
                ax.barh(grouped.index.astype(str), grouped.values)

            ax.set_xlabel(x_col)
            ax.set_ylabel(f"{agg}({y_col})")
            ax.set_title(f"{agg.title()} of {y_col} by {x_col} (Top {top_n})")

        elif chart_type == "Line":
            x_col = st.sidebar.selectbox("Select X-axis (Numeric)", numeric_cols)
            y_col = st.sidebar.selectbox("Select Y-axis (Numeric)", numeric_cols)

            ax.plot(df[x_col], df[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"Line: {y_col} vs {x_col}")

        elif chart_type == "Scatter":
            x_col = st.sidebar.selectbox("Select X-axis (Numeric)", numeric_cols)
            y_col = st.sidebar.selectbox("Select Y-axis (Numeric)", numeric_cols)

            ax.scatter(df[x_col], df[y_col], alpha=0.5)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"Scatter: {y_col} vs {x_col}")

        elif chart_type == "Histogram":
            col = st.sidebar.selectbox("Select Numeric Column", numeric_cols)
            bins = st.sidebar.slider("Bins", 10, 80, 30)

            ax.hist(df[col].dropna(), bins=bins)
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            ax.set_title(f"Histogram of {col}")

        elif chart_type == "Box Plot":
            col = st.sidebar.selectbox("Select Numeric Column", numeric_cols)

            ax.boxplot(df[col].dropna(), vert=False)
            ax.set_xlabel(col)
            ax.set_title(f"Box Plot of {col}")

        st.pyplot(fig)

