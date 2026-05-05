import streamlit as st
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

st.set_page_config(page_title="Linear Regression", layout="wide")
st.title("📈 Linear Regression — Price Predictor")
st.write("This app uses Linear Regression to predict Price based on a single input feature (Area).")

# ── Upload CSV ──
st.subheader("📂 Upload Dataset")
uploaded_file = st.file_uploader("price.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Dataset Preview")
    st.dataframe(df)

    # ── Dataset Info ──
    st.subheader("Dataset Info")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    # ── Column Selection ──
    st.subheader("🔧 Model Configuration")
    all_columns = df.columns.tolist()
    x_col = st.selectbox("Select Input Feature (X)", all_columns, index=0)
    y_col = st.selectbox("Select Target Column (Y)", all_columns, index=len(all_columns)-1)

    if x_col and y_col and x_col != y_col:
        x = df[[x_col]]
        y = df[y_col]

        # ── Train Model ──
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        reg = linear_model.LinearRegression()
        reg.fit(x_train, y_train)
        prediction = reg.predict(x_test)

        # ── Model Performance ──
        st.subheader("📊 Model Performance")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("R² Score", round(r2_score(y_test, prediction), 4))
        with col2:
            st.metric("MAE", round(mean_absolute_error(y_test, prediction), 4))
        with col3:
            st.metric("Intercept", round(float(reg.intercept_), 4))

        st.write("Coefficient:", round(float(reg.coef_[0]), 4))

        # ── Scatter Plot with Regression Line ──
        st.subheader("📉 Regression Line Plot")
        fig, ax = plt.subplots()
        ax.scatter(df[x_col], df[y_col], color="blue", alpha=0.6, label="Actual Data")
        ax.plot(df[x_col], reg.predict(df[[x_col]]), color="red", label="Regression Line")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.legend()
        st.pyplot(fig)

        # ── User Prediction ──
        st.subheader("🎯 Make a Prediction")
        user_input = st.number_input(f"Enter value for {x_col}", value=0.0)

        if st.button("Predict"):
            result = reg.predict([[user_input]])
            st.success(f"Predicted {y_col}: **{round(float(result[0]), 2)}**")

else:
    st.info("Please upload a CSV file to get started.")