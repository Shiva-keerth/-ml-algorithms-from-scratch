import streamlit as st
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Multiple Regression", layout="wide")
st.title("📈 Multiple Regression — Price Predictor")
st.write("This app uses Multiple Regression to predict the amount based on users and orders.")

# ── Upload CSV ──
st.subheader("📂 Upload Dataset")
uploaded_file = st.file_uploader("Book2.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.subheader("Dataset Info")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    # ── Define X and Y ──
    st.subheader("🔧 Model Configuration")
    all_columns = df.columns.tolist()
    target = st.selectbox("Select Target Column (Y)", all_columns, index=len(all_columns)-1)
    features = st.multiselect("Select Feature Columns (X)", [c for c in all_columns if c != target], default=[c for c in all_columns if c != target])

    if features and target:
        x = df[features]
        y = df[target]

        # ── Train Model ──
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        reg = linear_model.LinearRegression()
        reg.fit(x_train, y_train)
        prediction = reg.predict(x_test)

        # ── Model Performance ──
        st.subheader("📊 Model Performance")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("R² Score", round(r2_score(y_test, prediction), 4))
        with col2:
            st.metric("MAE", round(mean_absolute_error(y_test, prediction), 4))

        st.subheader("🧮 Model Coefficients")
        coef_df = pd.DataFrame({"Feature": features, "Coefficient": reg.coef_})
        st.dataframe(coef_df)
        st.write("Intercept:", round(reg.intercept_, 4))

        # ── User Prediction ──
        st.subheader("🎯 Make a Prediction")
        st.write("Enter values for each feature:")
        user_input = []
        cols = st.columns(len(features))
        for i, feature in enumerate(features):
            with cols[i]:
                val = st.number_input(f"{feature}", value=0.0)
                user_input.append(val)

        if st.button("Predict"):
            result = reg.predict([user_input])
            st.success(f"Predicted {target}: **{round(result[0], 2)}**")

else:
    st.info("Please upload a CSV file to get started.")