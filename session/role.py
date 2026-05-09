import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout= "wide")

if "users" not in st.session_state:
    st.session_state.users = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in =False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

def register():
    st.session_state.users.append({
        "username":st.session_state.reg_user,
        "password":st.session_state.reg_pass,
        "role":st.session_state.reg_role
    })
    st.success("Registration Successful")


def login():
    for user in st.session_state.users:
        if user["username"]==st.session_state.log_user and user["password"] == st.session_state.log_pass:
            st.session_state.logged_in = True
            st.session_state.current_user = user
        st.error("Invalid Details")

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None

if not st.session_state.logged_in:
    tab1,tab2 = st.tabs(["Login","Register"])


    with tab2:
        st.text_input("Username",key="reg_user")
        st.text_input("Password",key="reg_pass")
        st.selectbox("Role",["Student","Teacher"],key="reg_role")
        st.button("Register",on_click=register)

    with tab1:
        st.text_input("Username",key="log_user")
        st.text_input("Password",type="password",key="log_pass")
        st.button("Login",on_click=login)

else:
    user = st.session_state.current_user

    with st.sidebar:
        st.write(f"Welcome {user["username"]}")
        if user["role"] == "Student":
            selected = option_menu("Student Menu",["Dashboard","Course","Result"],
                                   icons=["house","book","clipboard-data"],default_index=0)
        elif user["role"] == "Teacher":
            selected = option_menu("Teacher Menu",["Dashboard","Manage Student","Upload Assignment"],
                                   icons=["house","people","upload"],default_index=0)

        st.button("Logout",on_click=logout)

    if selected == "Course":
        st.write("This Is The Course")
    if selected == "Result":
        st.write("This Is The Result")
    if selected == "Manage Student":
        st.write("This Is Manage Student")
    if selected == "Upload Assignment":
        st.write("Upload Your Assignment Here")