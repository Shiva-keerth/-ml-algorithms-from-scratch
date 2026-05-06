import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        "KNNCLASSIFIER",
        ["Dataset", "Prediction"],
        icons=["table", "activity"],
        menu_icon="cast",
        default_index=0
    )

if selected == "Dataset":
    df = pd.read_csv("improved_moviedataset.csv")
    st.write(df)

if selected == "Prediction":
    df = pd.read_csv("improved_moviedataset.csv")
    # data preprocessing
    le = LabelEncoder()
    df["genre"] = le.fit_transform(df["genre"])

    # define x and y
    x = df.drop("genre", axis=1)
    y = df["genre"]

    # train test and split
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.4, random_state=42)

    # scaling
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(xtrain)
    x_test_scaled = scaler.transform(xtest)

    # model initilization
    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(x_train_scaled, ytrain)

    # Accuracy
    y_pred = model.predict(x_test_scaled)
    accuracy = accuracy_score(ytest, y_pred)
    st.subheader("Model Accuracy")
    st.write(accuracy)

    # User prediction
    input1 = st.number_input("Enter runtime")
    input2 = st.number_input("Enter rating")

    if st.button("Predict (KNN)"):
        new_data = [[input1, input2]]
        new_data_scaled = scaler.transform(new_data)

        prediction = model.predict(new_data_scaled)
        transformed_prediction = le.inverse_transform(prediction)

        st.subheader("Prediction")
        st.write(transformed_prediction)
