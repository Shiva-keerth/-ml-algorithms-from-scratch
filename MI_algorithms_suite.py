import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        "ML Algorithms Suite",
        [
            "Linear Regression",
            "Multiple Linear Regression",
            "Decision Tree",
            "Random forest",
            "KNN Classifier",
            "K-Means Clustering"
        ],
        icons=["graph-up", "graph-up-arrow", "diagram-3", "tree", "people", "circle"],
        menu_icon="cpu",
        orientation="vertical",
        default_index=0
    )

if selected == "Linear Regression":
    df=pd.read_csv("price.csv")
    st.write(df)

    x = df[["Area"]]
    y = df[["Price"]]

    reg = linear_model.LinearRegression()
    reg.fit(x, y)

    input1 = st.number_input("enter the value1")
    if st.button("Predict (Linear Regression)"):
     prediction = reg.predict([[input1]])
     st.subheader("Prediction Value")
     st.write(prediction)

     st.write("Co-efficient")
     st.write(reg.coef_)
     st.write("Intercept")
     st.write(reg.intercept_)

if selected == "Multiple Linear Regression":
    df=pd.read_csv("Book2.csv")
    st.write(df)

    print(df[["users"]])
    print(df[["orders"]])

    x = df[["users", "orders"]]
    y = df[["amount"]]

    reg = linear_model.LinearRegression()
    reg.fit(x,y)

    input1=st.number_input("enter the value1")
    input2=st.number_input("enter the value2")
    if st.button("Predict (Multiple LR)"):
     prediction = reg.predict([[input1,input2]])
     st.write(prediction)
     st.subheader("Prediction Value")
     st.write(prediction)

     st.write("Co-efficient")
     st.write(reg.coef_)
     st.write("Intercept")
     st.write(reg.intercept_)

if selected == "Decision Tree":
    df = pd.read_csv("master_decision.csv")

    le = LabelEncoder()
    df["Placed"] = le.fit_transform(df["Placed"])
    df["GATE_Score"] = le.fit_transform(df["GATE_Score"])
    df["Should_Do_Masters"] = le.fit_transform(df["Should_Do_Masters"])

    st.write(df)

    x = df[["Placed", "GATE_Score", "Salary"]]
    y = df[["Should_Do_Masters"]]

    model = DecisionTreeClassifier()
    model.fit(x, y)

    input1 = st.number_input("enter the value1")
    input2 = st.number_input("enter the value2")
    input3 = st.number_input("enter the value3")
    if st.button("Predict (Decision Tree)"):
     new_data = [[input1, input2, input3]]
     predicition = model.predict(new_data)
     transformed_predicition = le.inverse_transform(predicition)
     st.subheader("Prediction")
     st.write(transformed_predicition)

if selected == "Random forest":
    df = pd.read_csv("master_decision.csv")

    le = LabelEncoder()
    df["GATE_Score"] = le.fit_transform(df["GATE_Score"])
    df["Should_Do_Masters"] = le.fit_transform(df["Should_Do_Masters"])

    st.write(df)

    x = df[["GATE_Score", "Salary"]]
    y = df["Should_Do_Masters"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(x_train, y_train)

    prediction = model.predict(x_test)
    st.subheader("Prediction")
    st.write(le.inverse_transform(prediction))

    accuracy = accuracy_score(y_test, prediction)
    st.subheader("Accuracy")
    st.write(accuracy)

    data1=st.number_input("Enter the value1")
    data2=st.number_input("Enter the value2")
    if st.button("Predict (Random forest)"):
     newdata = [[data1, data2]]
     newprediction = model.predict(newdata)
     st.write(le.inverse_transform(newprediction))

     accuracy = accuracy_score(y_test, prediction)
     st.subheader("Accuracy")
     st.write(accuracy)

if selected == "KNN Classifier":
    df = pd.read_csv("improved_moviedataset.csv")

    st.subheader("Dataset")
    st.write(df)

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
    st.subheader("Model Accuracy")
    st.write(accuracy)

    input1 = st.number_input("Enter runtime")
    input2 = st.number_input("Enter rating")

    if st.button("Predict (KNN)"):
        new_data = [[input1, input2]]
        new_data_scaled = scaler.transform(new_data)
        prediction = model.predict(new_data_scaled)
        transformed_prediction = le.inverse_transform(prediction)
        st.subheader("Prediction")
        st.write(transformed_prediction)

if selected == "K-Means Clustering":
    df = pd.read_csv("mall_customers.csv")

    st.subheader("Dataset")
    st.write(df)

    X = df[["Annual_Income", "Spending_Score"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42)
    y_kmeans = kmeans.fit_predict(X_scaled)

    df["Cluster"] = y_kmeans

    st.subheader("Cluster Plot")
    fig, ax1 = plt.subplots()
    ax1.scatter(X_scaled[:,0], X_scaled[:,1], c=y_kmeans, cmap='viridis')
    ax1.set_xlabel("Annual Income (Scaled)")
    ax1.set_ylabel("Spending Score (Scaled)")
    st.pyplot(fig)