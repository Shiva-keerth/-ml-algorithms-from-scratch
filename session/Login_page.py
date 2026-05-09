import streamlit as st
import pandas as pd
import os
import re
import time

FILE_NAME = "users.csv"
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["First Name","Last Name","Email","Phone","Username","Password"])
    df.to_csv(FILE_NAME, index=False)

if "page" not in st.session_state:
    st.session_state.page = "Login"
if "Logged in" in st.session_state:
    st.session_state.logged_in = False
if "Username" in st.session_state:
    st.session_state.username = ""

def signup_page():
    st.title("Sign Up Page")
    df = pd.read_csv(FILE_NAME)
    with st.form("Sign Up Form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        re_enter = st.text_input("Re-Enter Password", type="password")

        submit = st.form_submit_button("Sign Up")
        if st.form_submit_button("Already Registered ? Go To Login"):
            st.session_state.page = "Login"
            st.rerun()
        if submit:
            if not first_name or not last_name or not email or not phone or not username or not password or not re_enter:
                st.error("All fields are Mandatory")
            elif not re.match(r"^[\w\.-]+@[\w\.]+\.\w+$", email):
                st.error("Invalid Email Address")
            elif not re.match(r"^\d{10}$", phone):
                st.error("Phone Number must Carry 10 Digits")
            elif password != re_enter:
                st.error("Passwords do not match")
            elif len(password) < 8:
                st.error("Password must be at least 8 Characters")
            elif not re.search(r"[A-Z]", password):
                st.error("Capital Letter Missing")
            elif not re.search(r"[0-9]", password):
                st.error("Digit Missing")
            elif not re.search(r"[!@#$%^&*]", password):
                st.error("Special Character Missing")
            elif username in df["Username"].values:
                st.error("Username Already Exists")
            elif email in df["Email"].values:
                st.error("Email Already Exists")

            else:
                new_user = {
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Email": email,
                    "Phone": phone,
                    "Username": username,
                    "Password": password,
                }
                df = pd.concat([df,pd.DataFrame([new_user])],
                               ignore_index=True)
                df.to_csv(FILE_NAME, index=False)
                st.success("Registration Completed")
                time.sleep(1)
                st.session_state.page = "Login"
                st.rerun()

def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password")
    if st.button("Login"):
        df = pd.read_csv(FILE_NAME)
        user = df[(df["Username"] == username) & (df["Password"] == password)]
        if not user.empty:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "Home"
            st.rerun()
        else:
            st.error("Invalid Details")
    if st.button("New User? Register Here "):
        st.session_state.page = "Signup"
        st.rerun()

def home_page():
    st.title(f"Welcome {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "Login"
        st.rerun()
    tab1,tab2,tab3 = st.tabs(["Dashboard","Profile","Settings"])
    with tab1:
        st.header("Dashboard")
        st.write("Dashboard Related Content")
    with tab2:
        st.header("Profile")
        df = pd.read_csv(FILE_NAME)
        userdata = df[df["Username"] == st.session_state.username]
        st.write(userdata)
    with tab3:
        st.header("Settings")
        st.info("This Page is Under Development")

if st.session_state.page == "Login":
    login_page()
if st.session_state.page == "Signup":
    signup_page()
if st.session_state.page == "Home":
    if st.session_state.logged_in:
        home_page()
    else:
        st.session_state.page = "Login"
        st.rerun()