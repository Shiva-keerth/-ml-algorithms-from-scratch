import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn import linear_model
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="AI & ML Algorithms Suite", layout="wide")

# ── Custom CSS ──
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .algo-title {
        font-size: 2rem;
        font-weight: 800;
        color: #00d4ff;
        margin-bottom: 0.2rem;
    }
    .algo-desc {
        font-size: 1rem;
        color: #aaaaaa;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
        border-left: 4px solid #00d4ff;
        padding-left: 10px;
        margin: 1.5rem 0 0.8rem 0;
    }
    .result-box {
        background: linear-gradient(135deg, #1a4731, #0f2d1f);
        border: 1px solid #00ff88;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        color: #00ff88;
        margin-top: 1rem;
    }
    div[data-testid="metric-container"] {
        background: #1e1e2e;
        border: 1px solid #2e2e4e;
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🤖 AI & ML Suite")
    selected = option_menu(
        "",
        [
            "Linear Regression",
            "Multiple Regression",
            "Decision Tree",
            "Random Forest",
            "KNN Classifier",
            "K-Means Clustering"
        ],
        icons=["graph-up", "graph-up-arrow", "diagram-3", "tree-fill", "people-fill", "circle-half"],
        menu_icon="cpu-fill",
        orientation="vertical",
        default_index=0,
        styles={
            "container": {"background-color": "#1a1a2e"},
            "icon": {"color": "#00d4ff", "font-size": "16px"},
            "nav-link": {"color": "#cccccc", "font-size": "14px"},
            "nav-link-selected": {"background-color": "#0f3460", "color": "#00d4ff", "font-weight": "700"},
        }
    )

# ── 1. LINEAR REGRESSION ──
if selected == "Linear Regression":
    st.markdown('<div class="algo-title">📈 Linear Regression</div>', unsafe_allow_html=True)
    st.markdown('<div class="algo-desc">Predict Price based on a single input feature — Area</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV (price.csv)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.markdown('<div class="section-header">📋 Dataset Preview</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())

        x = df[["Area"]]
        y = df[["Price"]]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        reg = linear_model.LinearRegression()
        reg.fit(x_train, y_train)
        pred = reg.predict(x_test)

        st.markdown('<div class="section-header">📊 Model Performance</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("R² Score", round(r2_score(y_test, pred), 4))
        with col2:
            st.metric("MAE", round(mean_absolute_error(y_test, pred), 4))
        with col3:
            st.metric("Intercept", round(float(reg.intercept_[0]), 4))

        st.markdown('<div class="section-header">📉 Regression Line</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(facecolor='#1e1e2e')
        ax.set_facecolor('#1e1e2e')
        ax.scatter(df["Area"], df["Price"], color="#00d4ff", alpha=0.6, label="Actual Data")
        ax.plot(df["Area"], reg.predict(df[["Area"]]), color="#ff4b4b", linewidth=2, label="Regression Line")
        ax.set_xlabel("Area", color="white")
        ax.set_ylabel("Price", color="white")
        ax.tick_params(colors='white')
        ax.legend()
        st.pyplot(fig)

        st.markdown('<div class="section-header">🎯 Make a Prediction</div>', unsafe_allow_html=True)
        input1 = st.number_input("Enter Area (in sq.ft)", value=0.0)
        if st.button("Predict", key="lr"):
            prediction = reg.predict([[input1]])
            st.markdown(f'<div class="result-box">Predicted Price: ₹ {round(float(prediction[0][0]), 2)}</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Coefficient", round(float(reg.coef_[0][0]), 4))
            with col2:
                st.metric("Intercept", round(float(reg.intercept_[0]), 4))
    else:
        st.info("Please upload price.csv to get started.")

# ── 2. MULTIPLE REGRESSION ──
if selected == "Multiple Regression":
    st.markdown('<div class="algo-title">📊 Multiple Linear Regression</div>', unsafe_allow_html=True)
    st.markdown('<div class="algo-desc">Predict Amount based on multiple features — Users and Orders</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV (Book2.csv)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.markdown('<div class="section-header">📋 Dataset Preview</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())

        x = df[["users", "orders"]]
        y = df[["amount"]]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        reg = linear_model.LinearRegression()
        reg.fit(x_train, y_train)
        pred = reg.predict(x_test)

        st.markdown('<div class="section-header">📊 Model Performance</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("R² Score", round(r2_score(y_test, pred), 4))
        with col2:
            st.metric("MAE", round(mean_absolute_error(y_test, pred), 4))

        st.markdown('<div class="section-header">🎯 Make a Prediction</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            input1 = st.number_input("Enter Users", value=0.0)
        with col2:
            input2 = st.number_input("Enter Orders", value=0.0)
        if st.button("Predict", key="mlr"):
            prediction = reg.predict([[input1, input2]])
            st.markdown(f'<div class="result-box">Predicted Amount: ₹ {round(float(prediction[0][0]), 2)}</div>', unsafe_allow_html=True)
            st.metric("Intercept", round(float(reg.intercept_[0]), 4))
    else:
        st.info("Please upload Book2.csv to get started.")

# ── 3. DECISION TREE ──
if selected == "Decision Tree":
    st.markdown('<div class="algo-title">🌳 Decision Tree Classifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="algo-desc">Classify whether a student Should Do Masters based on Placement, GATE Score and Salary</div>', unsafe_allow_html=True)

    df = pd.read_csv("master_decision.csv")

    le = LabelEncoder()
    df["Placed"] = le.fit_transform(df["Placed"])
    df["GATE_Score"] = le.fit_transform(df["GATE_Score"])
    df["Should_Do_Masters"] = le.fit_transform(df["Should_Do_Masters"])

    st.markdown('<div class="section-header">📋 Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    x = df[["Placed", "GATE_Score", "Salary"]]
    y = df[["Should_Do_Masters"]]

    model = DecisionTreeClassifier()
    model.fit(x, y)

    st.markdown('<div class="section-header">🎯 Make a Prediction</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        input1 = st.number_input("Placed? No=0, Yes=1", value=0.0)
    with col2:
        input2 = st.number_input("GATE Score: AVG=0, GOOD=1, POOR=2", value=0.0)
    with col3:
        input3 = st.number_input("Enter Salary", value=0.0)
    if st.button("Predict", key="dt"):
        new_data = [[input1, input2, input3]]
        prediction = model.predict(new_data)
        transformed = le.inverse_transform(prediction)
        st.markdown(f'<div class="result-box">Should Do Masters: {transformed[0]}</div>', unsafe_allow_html=True)

# ── 4. RANDOM FOREST ──
if selected == "Random Forest":
    st.markdown('<div class="algo-title">🌲 Random Forest Classifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="algo-desc">Classify whether a student Should Do Masters using ensemble of 150 decision trees</div>', unsafe_allow_html=True)

    df = pd.read_csv("master_decision.csv")

    le = LabelEncoder()
    df["GATE_Score"] = le.fit_transform(df["GATE_Score"])
    df["Should_Do_Masters"] = le.fit_transform(df["Should_Do_Masters"])

    st.markdown('<div class="section-header">📋 Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    x = df[["GATE_Score", "Salary"]]
    y = df["Should_Do_Masters"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(x_train, y_train)
    prediction = model.predict(x_test)
    accuracy = accuracy_score(y_test, prediction)

    st.markdown('<div class="section-header">📊 Model Performance</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accuracy", f"{round(accuracy * 100, 2)}%")
    with col2:
        st.metric("Estimators", 150)
    with col3:
        st.metric("Test Size", "30%")

    st.markdown('<div class="section-header">📋 Test Predictions</div>', unsafe_allow_html=True)
    st.write(le.inverse_transform(prediction))

    st.markdown('<div class="section-header">🎯 Make a Prediction</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        data1 = st.number_input("GATE Score: AVG=0, GOOD=1, POOR=2", value=0.0)
    with col2:
        data2 = st.number_input("Enter Salary", value=0.0)
    if st.button("Predict", key="rf"):
        newdata = [[data1, data2]]
        newprediction = model.predict(newdata)
        st.markdown(f'<div class="result-box">Should Do Masters: {le.inverse_transform(newprediction)[0]}</div>', unsafe_allow_html=True)

# ── 5. KNN CLASSIFIER ──
if selected == "KNN Classifier":
    st.markdown('<div class="algo-title">👥 KNN Classifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="algo-desc">Classify movie genre based on Runtime and Rating using K-Nearest Neighbors</div>', unsafe_allow_html=True)

    df = pd.read_csv("improved_moviedataset.csv")

    st.markdown('<div class="section-header">📋 Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("K Neighbors", 4)

    le = LabelEncoder()
    df["genre"] = le.fit_transform(df["genre"])

    x = df.drop("genre", axis=1)
    y = df["genre"]

    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.4, random_state=42)

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(xtrain)
    x_test_scaled = scaler.transform(xtest)

    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(x_train_scaled, ytrain)

    y_pred = model.predict(x_test_scaled)
    accuracy = accuracy_score(ytest, y_pred)

    st.markdown('<div class="section-header">📊 Model Performance</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", f"{round(accuracy * 100, 2)}%")
    with col2:
        st.metric("Test Size", "40%")

    st.markdown('<div class="section-header">🎯 Make a Prediction</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        input1 = st.number_input("Enter Runtime (in minutes)", value=0.0)
    with col2:
        input2 = st.number_input("Enter Rating (1-10)", value=0.0)
    if st.button("Predict", key="knn"):
        new_data = [[input1, input2]]
        new_data_scaled = scaler.transform(new_data)
        prediction = model.predict(new_data_scaled)
        transformed_prediction = le.inverse_transform(prediction)
        st.markdown(f'<div class="result-box">Predicted Genre: {transformed_prediction[0]}</div>', unsafe_allow_html=True)

# ── 6. K-MEANS CLUSTERING ──
if selected == "K-Means Clustering":
    st.markdown('<div class="algo-title">⭕ K-Means Clustering</div>', unsafe_allow_html=True)
    st.markdown('<div class="algo-desc">Segment mall customers into clusters based on Annual Income and Spending Score</div>', unsafe_allow_html=True)

    df = pd.read_csv("mall_customers.csv")

    st.markdown('<div class="section-header">📋 Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Clusters (K)", 3)

    X = df[["Annual_Income", "Spending_Score"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42)
    y_kmeans = kmeans.fit_predict(X_scaled)
    df["Cluster"] = y_kmeans

    st.markdown('<div class="section-header">📊 Cluster Summary</div>', unsafe_allow_html=True)
    cluster_summary = df.groupby("Cluster")[["Annual_Income", "Spending_Score"]].mean().round(2)
    cluster_summary.index = [f"Cluster {i}" for i in cluster_summary.index]
    st.dataframe(cluster_summary, use_container_width=True)

    st.markdown('<div class="section-header">📉 Cluster Visualization</div>', unsafe_allow_html=True)
    colors = ["#00d4ff", "#ff4b4b", "#00ff88"]
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#1e1e2e')
    ax.set_facecolor('#1e1e2e')
    for i in range(3):
        mask = y_kmeans == i
        ax.scatter(X_scaled[mask, 0], X_scaled[mask, 1],
                  color=colors[i], label=f"Cluster {i}", alpha=0.8, s=60)
    ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
              color='white', marker='X', s=200, label='Centroids', zorder=5)
    ax.set_xlabel("Annual Income (Scaled)", color="white")
    ax.set_ylabel("Spending Score (Scaled)", color="white")
    ax.set_title("Customer Segments", color="white", fontsize=14)
    ax.tick_params(colors='white')
    ax.legend(facecolor='#2e2e2e', labelcolor='white')
    st.pyplot(fig)