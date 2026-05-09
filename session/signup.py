import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="Signup")
st.title("Create you account")

FILE_NAME="user.csv"

if not os.path.exists(FILE_NAME):
    df=pd.DataFrame(columns=["First Name","Last Name","Email","Phone","Username","Password"])
    df.to_csv(FILE_NAME,index=False)

    if "signup_success" not in st.session_state:
        st.session_state.signup_success =False

with st.form("Signup Form"):
    first_name=st.text_input("First Name")
    last_name=st.text_input("Last Name")
    email=st.text_input("Email")
    phone=st.text_input("Phone")
    username=st.text_input("Username")
    password=st.text_input("Password")
    re_enter=st.text_input("Re_Enter Password",type="password")

    submit=st.form_submit_button("Sign up")
    if submit:
        if not first_name or not last_name or not email or not phone or not username or not password or not re_enter:
            st.error("All the fields are mandatory")
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$",email):
            st.error("Email is invalid")
        elif not re.match(r"^\d{10}$",phone):
            st.error("Phone must contain 10 digits")
        elif password != re_enter:
            st.error("Password does not match")
        elif len(password) < 8:
            st.error("Password must contain 8 characters")
        elif not re.search(r"[A-Z]",password):
            st.error("Capital letter missing")
        elif not re.search(r"[!@#$%^&*]",password):
            st.error("Special character missing")
        else:

            df=pd.read_csv(FILE_NAME)

            if email in df["Email"].values:
                st.error("Email already exists")
            elif username in df["Username"].values:
                st.error("Username already exists")
            else:
                new_data={
                    "First Name":first_name,
                    "Last Name":last_name,
                    "Email":email,
                    "Phone":phone,
                    "Username":username,
                    "Password":password
                }
                df=pd.concat([df,pd.DataFrame([new_data])],ignore_index=True)
                df.to_csv(FILE_NAME,index=False)
                st.session_state.signup_success =True
            if st.session_state.signup_success:
                st.success("Account Created")
