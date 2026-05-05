import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model
import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

with st.sidebar:
    selected=option_menu("Streamlit display",["Linear Regression","Multiple Linear Regression","Decision Tree","Random forest"],icons=["table","table","table","table"],menu_icon=["cast"],orientation="vertical",default_index=0)

if selected == "Linear Regression":
    df=pd.read_csv("price.csv")
    st.write(df)

    x = df[["Area"]]
    y = df[["Price"]]

    # model selection

    reg = linear_model.LinearRegression()

    # fit data into model

    reg.fit(x, y)

    # prediction
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

    # define x and y

    x = df[["users", "orders"]]
    y = df[["amount"]]

    # model selection

    reg = linear_model.LinearRegression()

    # fit data into model

    reg.fit(x,y)

    # prediction
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

    # data preprocessing
    # label encoding

    # st.write(df["Placed"])

    le = LabelEncoder()
    df["Placed"] = le.fit_transform(df["Placed"])
    df["GATE_Score"] = le.fit_transform(df["GATE_Score"])
    df["Should_Do_Masters"] = le.fit_transform(df["Should_Do_Masters"])

    st.write(df)

    # define x and y
    x = df[["Placed", "GATE_Score", "Salary"]]
    y = df[["Should_Do_Masters"]]

    #  model selection
    model = DecisionTreeClassifier()

    # fit data into model
    model.fit(x, y)

    # prediction
    # Placed -- No(0),Yes(1)
    # Gate Score -- AVG(0),GOOD(1),POOR(2)
    input1 = st.number_input("enter the value1")
    input2 = st.number_input("enter the value2")
    input3 = st.number_input("enter the value3")
    if st.button("Predict (Decision Tree)"):
     new_data = [[input1, input2, input3]]
     predicition = model.predict(new_data)
    # print(prediciton)

     transformed_predicition = le.inverse_transform(predicition)
     st.subheader("Prediction")
     st.write(transformed_predicition)

if selected == "Random forest":

    # file read
    df = pd.read_csv("master_decision.csv")

    # data preprocess

    le = LabelEncoder()
    df["GATE_Score"] = le.fit_transform(df["GATE_Score"])
    df["Should_Do_Masters"] = le.fit_transform(df["Should_Do_Masters"])

    st.write(df)

    # define x and y

    x = df[["GATE_Score", "Salary"]]
    y = df["Should_Do_Masters"]

    # train and test splitting

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    # model initialize
    model = RandomForestClassifier(n_estimators=150, random_state=42)

    # fit data into model
    model.fit(x_train, y_train)

    # prediction
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