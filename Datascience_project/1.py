# # import streamlit as st
# # from streamlit_option_menu import option_menu
# # import pandas as pd
# # import plotly.express as px
# # from sklearn.preprocessing import LabelEncoder
# # from sklearn.ensemble import RandomForestClassifier
# # from sklearn.metrics import accuracy_score
# # from sklearn.model_selection import train_test_split
# #
# # st.set_page_config(page_title="Workforce Readiness Predictor", layout="wide")
# # file_name="intern dataset.csv"
# #
# # if 'df' not in st.session_state:
# #     st.session_state.df = pd.read_csv("intern dataset.csv")
# #
# # df = st.session_state.df
# #
# # def save_data():
# #     st.session_state.df.to_csv("intern dataset.csv", index=False)
# #
# #
# #
# # with st.sidebar:
# #     selected = option_menu(
# #         menu_title="Main Menu",
# #         options=["Dataset", "Overview","Add New Employee","View Employee","AI Model Insights"],
# #         icons=["table", "bar-chart","person-plus", "person-lines-fill","robot"],
# #         menu_icon="briefcase",
# #         default_index=0
# #     )
# #
# # if selected == "Dataset":
# #
# #     st.title("Dataset Explorer")
# #
# #     st.divider()
# #
# #     col1, col2, col3 = st.columns(3)
# #
# #     col1.metric("Total Rows", df.shape[0])
# #     col2.metric("Total Columns", df.shape[1])
# #     col3.metric("Missing Values", df.isna().sum().sum())
# #
# #     st.divider()
# #
# #     # column selection
# #     selected_columns = st.multiselect(
# #         "Choose columns to display",
# #         df.columns,
# #         default=df.columns
# #     )
# #
# #     filtered_df = df[selected_columns]
# #
# #     # search dataset
# #     st.subheader("Search in Dataset")
# #
# #     search_value = st.text_input("Search Any Value")
# #
# #     if search_value:
# #         filtered_df = filtered_df[
# #             filtered_df.astype(str).apply(
# #                 lambda row: row.str.contains(search_value, case=False).any(),
# #                 axis=1
# #             )
# #         ]
# #
# #     # column filter
# #     st.subheader("Column Filter")
# #
# #     col1, col2 = st.columns(2)
# #
# #     with col1:
# #         filter_column = st.selectbox("Select Column", filtered_df.columns)
# #
# #     with col2:
# #         filter_value = st.selectbox(
# #             "Select Value",
# #             filtered_df[filter_column].dropna().unique()
# #         )
# #
# #     if st.button("Apply Filter"):
# #         filtered_df = filtered_df[filtered_df[filter_column] == filter_value]
# #
# #     st.divider()
# #
# #     # row display
# #     st.subheader("Row display")
# #
# #     rows = st.slider(
# #         "Number of row display",
# #         min_value=10,
# #         max_value=len(filtered_df),
# #         value=100
# #     )
# #
# #     # dataset table
# #     st.subheader("Dataset Table")
# #     st.dataframe(filtered_df.head(rows), use_container_width=True)
# #
# #     # show full dataset
# #     if st.checkbox("Show all dataset"):
# #         st.dataframe(df, use_container_width=True)
# #
# #     st.divider()
# #
# #     # columns statistics
# #     numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
# #
# #     if len(numeric_cols) > 0:
# #         selected_col = st.selectbox("Select Numeric Column", numeric_cols)
# #         st.write(filtered_df[selected_col].describe())
# #
# #     st.divider()
# #
# #     # download dataset
# #     st.subheader("Download dataset")
# #
# #     csv = filtered_df.to_csv(index=False).encode("utf-8")
# #
# #     st.download_button(
# #         "Download Dataset",
# #         csv,
# #         file_name="dataset.csv",
# #         mime="text/csv"
# #     )
# #
# # if selected == "Overview":
# #     st.title("👥 Workforce Readiness: Strategic Talent Overview")
# #
# #     total_employees = len(df)
# #     avg_engagement = df["Engagement_Score"].mean()
# #     high_risk_count = df[df["Attrition_Risk_Level"] == 'High'].shape[0]
# #     risk_rate = (high_risk_count / total_employees * 100) if total_employees > 0 else 0
# #     avg_completion = df["Task_Completion_Rate"].mean()
# #
# #     kpi1, kpi2, kpi3, kpi4 = st.columns(4)
# #     kpi1.metric(label="Total Workforce", value=f"{total_employees:,}")
# #     kpi2.metric(label="Avg Engagement Score", value=f"{avg_engagement:.1f}/100")
# #     kpi3.metric(label="Critical Attrition Risk", value=f"{risk_rate:.1f}%", delta="High Risk", delta_color="inverse")
# #     kpi4.metric(label="Task Efficiency", value=f"{avg_completion:.1f}%")
# #
# #     st.divider()
# #
# #     col_trend, col_attrition = st.columns(2)
# #
# #     with col_trend:
# #         st.subheader("Performance Trend Distribution")
# #         trend_dist = df["Performance_Trend"].value_counts().to_frame(name="Count")
# #         trend_dist["Share %"] = (trend_dist["Count"] / total_employees * 100)
# #         st.dataframe(trend_dist.style.format({"Share %": "{:.1f}%"}), use_container_width=True)
# #
# #     with col_attrition:
# #         st.subheader("Attrition Risk Audit")
# #         attrition_dist = df["Attrition_Risk_Level"].value_counts().to_frame(name="Count")
# #         # Color coding: Red/Orange for risk visualization
# #         st.bar_chart(attrition_dist, color="#ff4b4b")
# #
# # # ADD NEW EMPLOYEE
# #
# # elif selected == "Add New Employee":
# #     st.title("Add New Employee")
# #     st.markdown(
# #         "Enter the metrics for the new hire. The system will train the Random Forest and predict their Performance Trend.")
# #
# #     # Auto-generate next Employee ID based on row count
# #     next_id_num = len(st.session_state.df) + 1
# #     default_emp_id = f"EMP_{str(next_id_num).zfill(5)}"
# #
# #     with st.form("add_employee_form", clear_on_submit=True):
# #         col1, col2 = st.columns(2)
# #
# #         with col1:
# #             emp_id = st.text_input("Employee ID", default_emp_id)
# #             tech_score = st.number_input("Technical Assessment Score (0-100)", 0, 100, 75)
# #             coding_score = st.number_input("Coding Test Score (0-100)", 0, 100, 70)
# #             quiz_score = st.number_input("Average Quiz Score (0-100)", 0, 100, 75)
# #             task_comp = st.number_input("Task Completion Rate %", 0.0, 100.0, 85.0)
# #             manager_feedback = st.number_input("Mentor Feedback Rating (1.0-5.0)", 1.0, 5.0, 3.8, 0.1)
# #
# #         with col2:
# #             attendance = st.number_input("Attendance Rate %", 0.0, 100.0, 90.0)
# #             study_hours = st.number_input("Weekly Learning Hours", 0.0, 60.0, 15.0)
# #             screen_time = st.number_input("Daily Screen Time Hours", 0.0, 24.0, 7.5, step=0.5)
# #             stress_level = st.number_input("Stress Level (0.0-10.0)", 0.0, 10.0, 4.5, step=0.1)
# #             engagement = st.number_input("Engagement Score (0-100)", 0.0, 100.0, 75.0)
# #
# #         submitted = st.form_submit_button("Save Employee & Run ML Prediction")
# #
# #         if submitted:
# #             with st.spinner("Training Random Forest & Making Prediction..."):
# #                 # --- YOUR EXACT ML STRUCTURE STARTS HERE ---
# #                 # file read
# #                 ml_df = pd.read_csv("intern dataset.csv")
# #
# #                 # data preprocess
# #                 le = LabelEncoder()
# #                 ml_df["Performance_Trend"] = le.fit_transform(ml_df["Performance_Trend"])
# #
# #                 # define x and y
# #                 x = ml_df[[
# #                     'Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score',
# #                     'Task_Completion_Rate', 'Attendance_Rate', 'Weekly_Learning_Hours',
# #                     'Daily_Screen_Time_Hours', 'Stress_Level', 'Engagement_Score',
# #                     'Mentor_Feedback_Rating'
# #                 ]]
# #                 y = ml_df["Performance_Trend"]
# #
# #                 # train and test splitting
# #                 x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
# #
# #                 # model initialize
# #                 model = RandomForestClassifier(n_estimators=150, random_state=42)
# #
# #                 # fit data into model
# #                 model.fit(x_train, y_train)
# #
# #                 # prediction on new data (double brackets for 2D array)
# #                 newdata = [[
# #                     tech_score, coding_score, quiz_score, task_comp,
# #                     attendance, study_hours, screen_time, stress_level,
# #                     engagement, manager_feedback
# #                 ]]
# #
# #                 newprediction = model.predict(newdata)
# #                 predicted_trend = le.inverse_transform(newprediction)[0]
# #                 # --- YOUR EXACT ML STRUCTURE ENDS HERE ---
# #
# #             # Create new row dictionary to save
# #             new_row = {
# #                 'Employee_ID': emp_id,
# #                 'Company_Name': 'Pending',
# #                 'Department': 'Pending',
# #                 'Role': 'New Hire',
# #                 'Education_Level': 'Pending',
# #                 'University_Tier': 'Pending',
# #                 'Internship_Duration_Months': 0,
# #                 'Technical_Assessment_Score': tech_score,
# #                 'Coding_Test_Score': coding_score,
# #                 'Average_Quiz_Score': quiz_score,
# #                 'Project_Evaluation_Score': 0,  # Default for new hire
# #                 'Weekly_Learning_Hours': study_hours,
# #                 'Daily_Screen_Time_Hours': screen_time,
# #                 'Task_Completion_Rate': task_comp,
# #                 'Assignment_Submission_Rate': 0,  # Default for new hire
# #                 'Attendance_Rate': attendance,
# #                 'Engagement_Score': engagement,
# #                 'Peer_Feedback_Rating': 0.0,  # Default for new hire
# #                 'Mentor_Feedback_Rating': manager_feedback,
# #                 'Stress_Level': stress_level,
# #                 'Fatigue_Index': 0.0,  # Default
# #                 'Skill_Growth_Index': 0.0,  # Default
# #                 'Readiness_Score': 75.0,  # Default Placeholder
# #                 'Performance_Trend': predicted_trend,  # THE AI PREDICTION
# #                 'Attrition_Risk_Level': 'Medium'  # Default Placeholder
# #             }
# #
# #             # Save to Session State and overwrite CSV
# #             new_df = pd.DataFrame([new_row])
# #             st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
# #             save_data()
# #
# #             st.success(f"Employee {emp_id} added successfully!")
# #             st.info(f"AI Predicted Performance Trend: **{predicted_trend}**")
# #
# # # view employee
# #
# # elif selected == "View Employee":
# #     st.title("View Employee Details")
# #
# #     employee_list = st.session_state.df['Employee_ID'].tolist()
# #     selected_emp = st.selectbox("Search / Select Employee ID", reversed(employee_list))
# #
# #     if selected_emp:
# #         emp_data = st.session_state.df[st.session_state.df['Employee_ID'] == selected_emp].iloc[0]
# #
# #         st.markdown(f"### Profile: {selected_emp}")
# #
# #         st.subheader("🤖 AI Assessment")
# #         st.metric("Predicted Performance Trend", emp_data['Performance_Trend'])
# #
# #         st.markdown("---")
# #
# #         st.subheader("Core Metrics")
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             st.write(f"**Technical Assessment:** {emp_data['Technical_Assessment_Score']}")
# #             st.write(f"**Coding Test Score:** {emp_data['Coding_Test_Score']}")
# #             st.write(f"**Task Completion:** {emp_data['Task_Completion_Rate']}%")
# #             st.write(f"**Attendance:** {emp_data['Attendance_Rate']}%")
# #         with col2:
# #             st.write(f"**Stress Level:** {emp_data['Stress_Level']}/10")
# #             st.write(f"**Daily Screen Time:** {emp_data['Daily_Screen_Time_Hours']} hrs")
# #             st.write(f"**Weekly Learning:** {emp_data['Weekly_Learning_Hours']} hrs")
# #             st.write(f"**Mentor Feedback:** {emp_data['Mentor_Feedback_Rating']}/5.0")
# #
# # # random forest
# # elif selected == "AI Model Insights":
# #     st.title("🧠 AI Model Insights")
# #     st.markdown("Training the Random Forest model using your exact step-by-step structure.")
# #
# #     # 1. file read
# #     df = pd.read_csv("intern dataset.csv")
# #
# #     # 2. data preprocess (Encoding the Target 'Performance_Trend')
# #     le = LabelEncoder()
# #     df["Performance_Trend"] = le.fit_transform(df["Performance_Trend"])
# #
# #     st.write("Data Preview:")
# #     st.dataframe(df.head())
# #
# #     # 3. define x and y
# #     x = df[[
# #         'Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score',
# #         'Task_Completion_Rate', 'Attendance_Rate', 'Weekly_Learning_Hours',
# #         'Daily_Screen_Time_Hours', 'Stress_Level', 'Engagement_Score',
# #         'Mentor_Feedback_Rating'
# #     ]]
# #     y = df["Performance_Trend"]
# #
# #     # 4. train and test splitting
# #     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
# #
# #     # 5. model initialize
# #     model = RandomForestClassifier(n_estimators=150, random_state=42)
# #
# #     # 6. fit data into model
# #     with st.spinner("Training model..."):
# #         model.fit(x_train, y_train)
# #
# #     # 7. prediction
# #     prediction = model.predict(x_test)
# #
# #     st.write("Test Set Predictions:")
# #     st.write(le.inverse_transform(prediction))
# #
# #     accuracy = accuracy_score(y_test, prediction)
# #     st.write(f"**Accuracy:** {accuracy}")
# #
# #     # 8. prediction on new data (Using a sample intern's metrics in double brackets)
# #     st.write("Prediction on New Data:")
# #
# #     # 10 metrics matching your x variables
# #     newdata = [[88, 85, 90, 95.0, 98.0, 20.0, 6.0, 3.5, 85.0, 4.2]]
# #
# #     newprediction = model.predict(newdata)
# #     st.success(f"New Employee Performance Trend: **{le.inverse_transform(newprediction)[0]}**")
#
# import streamlit as st
# from streamlit_option_menu import option_menu
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# import smtplib
# import random
# import hashlib
# from email.mime.text import MIMEText
# from fpdf import FPDF
# import base64
#
# st.set_page_config(page_title="Workforce Readiness Platform", layout="wide")
#
# # --- INJECTING THE PREMIUM UI CSS DIRECTLY ---
# st.markdown("""
# <style>
# /* =========================================
#    WORKFORCE PORTAL - PREMIUM UI THEME
# ========================================= */
#
# /* Hide Streamlit default header and footer for a clean app look */
# header {visibility: hidden;}
# footer {visibility: hidden;}
#
# /* --- FLOATING METRIC CARDS --- */
# [data-testid="stMetric"] {
#     background: linear-gradient(145deg, #1e2235, #171a28);
#     border-radius: 15px;
#     padding: 20px;
#     box-shadow: 5px 5px 15px rgba(0,0,0,0.2), -5px -5px 15px rgba(255,255,255,0.02);
#     border: 1px solid rgba(255,255,255,0.05);
#     transition: transform 0.3s ease;
# }
#
# [data-testid="stMetric"]:hover {
#     transform: translateY(-5px);
# }
#
# [data-testid="stMetricValue"] {
#     font-size: 2rem !important;
#     font-weight: 800 !important;
#     color: #ffffff !important;
# }
#
# /* --- MODERN INPUT FIELDS --- */
# .stTextInput > div > div > input {
#     border-radius: 10px;
#     border: 1px solid rgba(255,255,255,0.1) !important;
#     padding: 10px 15px !important;
#     background-color: rgba(0,0,0,0.2) !important;
#     transition: all 0.3s ease;
# }
#
# .stTextInput > div > div > input:focus {
#     border: 1px solid #4CAF50 !important;
#     box-shadow: 0 0 10px rgba(76, 175, 80, 0.3) !important;
# }
#
# /* --- GRADIENT PRIMARY BUTTONS --- */
# .stButton > button[kind="primary"] {
#     background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
#     color: white !important;
#     border: none !important;
#     border-radius: 10px !important;
#     padding: 0.5rem 1rem !important;
#     font-weight: 600 !important;
#     box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
#     transition: all 0.3s ease !important;
# }
#
# .stButton > button[kind="primary"]:hover {
#     transform: translateY(-2px) !important;
#     box-shadow: 0 6px 15px rgba(76, 175, 80, 0.4) !important;
# }
#
# /* --- SECONDARY/STANDARD BUTTONS --- */
# .stButton > button[kind="secondary"] {
#     border-radius: 10px !important;
#     border: 1px solid rgba(255,255,255,0.2) !important;
#     background-color: transparent !important;
#     transition: all 0.3s ease !important;
# }
#
# .stButton > button[kind="secondary"]:hover {
#     border-color: #ffffff !important;
#     background-color: rgba(255,255,255,0.05) !important;
# }
#
# /* --- SIDEBAR GLOW EFFECT --- */
# [data-testid="stSidebar"] {
#     border-right: 1px solid rgba(255,255,255,0.05);
#     background: linear-gradient(180deg, rgba(14,17,23,1) 0%, rgba(22,26,38,1) 100%);
# }
#
# /* --- FORM CONTAINERS --- */
# [data-testid="stForm"] {
#     border-radius: 15px;
#     border: 1px solid rgba(255,255,255,0.1);
#     background-color: rgba(255,255,255,0.02);
#     padding: 20px;
# }
# </style>
# """, unsafe_allow_html=True)
# # -------------------------------------
#
# # ==========================================
# # ⚙️ CONFIGURATION & HELPER FUNCTIONS
# # ==========================================
# SENDER_EMAIL = "your_email@gmail.com"
# EMAIL_AUTH_VAR = "your_sixteen_digit_app_str"
#
# USER_FILE = "users.csv"
# FILE_NAME = "intern dataset.csv"
#
# def init_db():
#     try:
#         pd.read_csv(USER_FILE)
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["Email", "Password", "Role", "Employee_ID"])
#         df.to_csv(USER_FILE, index=False)
#
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()
#
# def send_otp_email(receiver_email, otp):
#     try:
#         msg = MIMEText(f"Your Workforce Portal verification code is: {otp}")
#         msg['Subject'] = 'Portal Registration OTP'
#         msg['From'] = SENDER_EMAIL
#         msg['To'] = receiver_email
#         server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.sendmail(SENDER_EMAIL, [receiver_email], msg.as_string())
#         server.quit()
#         return True
#     except Exception:
#         print(f"\n⚠️ EMAIL FAILED. Developer Mode OTP for {receiver_email} is: {otp}\n")
#         return False
#
# def save_data():
#     st.session_state.df.to_csv(FILE_NAME, index=False)
#
# # Initialize states
# init_db()
# if "logged_in" not in st.session_state: st.session_state.logged_in = False
# if "otp" not in st.session_state: st.session_state.otp = None
# if "register_data" not in st.session_state: st.session_state.register_data = None
#
# # ==========================================
# # 🛑 UNAUTHENTICATED VIEW (LOGIN/REGISTER)
# # ==========================================
# if not st.session_state.logged_in:
#     _, col_mid, _ = st.columns([1, 2, 1])
#
#     with col_mid:
#         st.title("🔐 Workforce Portal")
#         tab1, tab2 = st.tabs(["Login", "Register"])
#
#         with tab1:
#             login_email = st.text_input("Email", key="login_email")
#             login_pass = st.text_input("Password", type="password", key="login_pass")
#             if st.button("Login", type="primary", use_container_width=True):
#                 users_df = pd.read_csv(USER_FILE)
#                 hashed_input = hash_password(login_pass)
#                 user = users_df[(users_df['Email'] == login_email) & (users_df['Password'] == hashed_input)]
#
#                 if not user.empty:
#                     st.session_state.logged_in = True
#                     st.session_state.role = user.iloc[0]['Role']
#                     st.session_state.user_email = user.iloc[0]['Email']
#                     st.session_state.emp_id = user.iloc[0]['Employee_ID']
#                     st.rerun()
#                 else:
#                     st.error("Invalid Email or Password")
#
#         with tab2:
#             reg_email = st.text_input("Work Email")
#             reg_pass = st.text_input("Password", type="password")
#             reg_role = st.selectbox("Register as:", ["Intern", "HR"])
#
#             reg_emp_id = "N/A"
#             if reg_role == "Intern":
#                 reg_emp_id = st.text_input("Your Employee ID (e.g., EMP_00001)")
#
#             if st.button("Send Verification Code", use_container_width=True):
#                 users_df = pd.read_csv(USER_FILE)
#                 if reg_email in users_df['Email'].values:
#                     st.error("Email is already registered!")
#                 elif reg_role == "Intern" and not reg_emp_id:
#                     st.error("Interns must provide their Employee ID.")
#                 else:
#                     st.session_state.otp = str(random.randint(100000, 999999))
#                     st.session_state.register_data = {
#                         "Email": reg_email, "Password": hash_password(reg_pass),
#                         "Role": reg_role, "Employee_ID": reg_emp_id
#                     }
#                     if send_otp_email(reg_email, st.session_state.otp):
#                         st.success("OTP sent to your email!")
#                     else:
#                         st.warning("Check your terminal for the OTP!")
#
#             if st.session_state.otp:
#                 entered_otp = st.text_input("Enter 6-digit OTP", max_chars=6)
#                 if st.button("Verify & Register", type="primary"):
#                     if entered_otp == st.session_state.otp:
#                         new_user = pd.DataFrame([st.session_state.register_data])
#                         new_user.to_csv(USER_FILE, mode='a', header=False, index=False)
#                         st.success("Account created! You can now Login.")
#                         st.session_state.otp = None
#                     else:
#                         st.error("Incorrect OTP.")
#
# # ==========================================
# # ✅ AUTHENTICATED VIEW (THE PLATFORM)
# # ==========================================
# else:
#     if 'df' not in st.session_state:
#         try:
#             st.session_state.df = pd.read_csv(FILE_NAME)
#         except FileNotFoundError:
#             st.error(f"Cannot find {FILE_NAME}")
#             st.stop()
#
#     df = st.session_state.df
#
#     with st.sidebar:
#         st.markdown(f"### 👤 Profile")
#         st.write(f"**Email:** {st.session_state.user_email}")
#         st.write(f"**Role:** {st.session_state.role}")
#         if st.session_state.role == "Intern":
#             st.write(f"**ID:** {st.session_state.emp_id}")
#         st.divider()
#
#     # ==========================================
#     # 👨‍💼 HR PORTAL
#     # ==========================================
#     if st.session_state.role == "HR":
#         with st.sidebar:
#             selected = option_menu(
#                 "HR Menu",
#                 ["Overview", "Add New Employee", "View Employee", "Compare Employees", "Remove Employee", "AI Model Insights"],
#                 icons=["bar-chart", "person-plus", "person-lines-fill", "people-fill", "person-x", "robot"],
#                 default_index=0
#             )
#
#         if selected == "Overview":
#             st.title("👥 Workforce Readiness: Strategic Talent Overview")
#             total_employees = len(df)
#             avg_engagement = df["Engagement_Score"].mean()
#             high_risk_count = df[df["Attrition_Risk_Level"] == 'High'].shape[0] if "Attrition_Risk_Level" in df.columns else 0
#             risk_rate = (high_risk_count / total_employees * 100) if total_employees > 0 else 0
#             avg_completion = df["Task_Completion_Rate"].mean()
#
#             kpi1, kpi2, kpi3, kpi4 = st.columns(4)
#             kpi1.metric("Total Workforce", f"{total_employees:,}")
#             kpi2.metric("Avg Engagement", f"{avg_engagement:.1f}/100")
#             kpi3.metric("Critical Attrition Risk", f"{risk_rate:.1f}%", delta="High Risk", delta_color="inverse")
#             kpi4.metric("Task Efficiency", f"{avg_completion:.1f}%")
#
#             st.divider()
#             col_trend, col_attrition = st.columns(2)
#             with col_trend:
#                 st.subheader("Performance Trend Distribution")
#                 trend_dist = df["Performance_Trend"].value_counts().to_frame(name="Count")
#                 trend_dist["Share %"] = (trend_dist["Count"] / total_employees * 100)
#                 st.dataframe(trend_dist.style.format({"Share %": "{:.1f}%"}), use_container_width=True)
#             with col_attrition:
#                 st.subheader("Attrition Risk Audit")
#                 if "Attrition_Risk_Level" in df.columns:
#                     attrition_dist = df["Attrition_Risk_Level"].value_counts().to_frame(name="Count")
#                     st.bar_chart(attrition_dist, color="#ff4b4b")
#
#         elif selected == "Add New Employee":
#             st.title("Add New Employee")
#             st.markdown("Enter the static day-one details below. **The RPA Bot will automatically track their weekly metrics!**")
#
#             next_id_num = len(st.session_state.df) + 1
#             default_emp_id = f"EMP_{str(next_id_num).zfill(5)}"
#             dept_options = st.session_state.df['Department'].dropna().unique().tolist()
#             if not dept_options: dept_options = ["Data Analytics", "Engineering", "HR"]
#
#             with st.form("add_employee_form", clear_on_submit=True):
#                 st.subheader("Basic Information")
#                 col_a, col_b, col_c = st.columns(3)
#                 with col_a: emp_id = st.text_input("Employee ID", default_emp_id)
#                 with col_b: emp_name = st.text_input("Employee Name", "John Doe")
#                 with col_c: emp_email = st.text_input("Employee Email", "john.doe@company.com")
#
#                 col_d, col_e = st.columns(2)
#                 with col_d: emp_dept = st.selectbox("Department", dept_options)
#                 with col_e: internship_duration = st.number_input("Internship Duration (Months)", 1, 24, 6)
#
#                 st.divider()
#                 st.subheader("Static Technical Scores (Day 1)")
#                 col1, col2, col3 = st.columns(3)
#                 with col1: tech_score = st.number_input("Tech Assessment (0-100)", 0, 100, 75)
#                 with col2: coding_score = st.number_input("Coding Test (0-100)", 0, 100, 70)
#                 with col3: quiz_score = st.number_input("Initial Quiz Score (0-100)", 0, 100, 75)
#
#                 st.divider()
#                 st.info("🤖 **Automation Active:** Weekly tracking metrics will be automatically populated by the RPA Bot.")
#
#                 if st.form_submit_button("Save Employee Data"):
#                     new_row = {
#                         'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Employee_Email': emp_email,
#                         'Department': emp_dept, 'Company_Name': 'Pending', 'Role': 'New Hire',
#                         'Internship_Duration_Months': internship_duration, 'Technical_Assessment_Score': tech_score,
#                         'Coding_Test_Score': coding_score, 'Average_Quiz_Score': quiz_score,
#                         'Task_Completion_Rate': 0.0, 'Attendance_Rate': 0.0, 'Weekly_Learning_Hours': 0.0,
#                         'Daily_Screen_Time_Hours': 0.0, 'Stress_Level': 0.0, 'Engagement_Score': 0.0,
#                         'Mentor_Feedback_Rating': 0.0, 'Performance_Trend': 'Pending AI Assessment', 'Attrition_Risk_Level': 'Pending'
#                     }
#                     new_df = pd.DataFrame([new_row])
#                     st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
#                     save_data()
#                     st.success(f"Employee {emp_name} added successfully!")
#
#         elif selected == "View Employee":
#             st.title("View Employee Details")
#             employee_list = st.session_state.df['Employee_ID'].tolist()
#             selected_emp = st.selectbox("Select Employee", reversed(employee_list))
#
#             if selected_emp:
#                 emp_data = st.session_state.df[st.session_state.df['Employee_ID'] == selected_emp].iloc[0]
#                 st.markdown(f"### Profile: {selected_emp}")
#                 name = emp_data.get('Employee_Name', 'N/A')
#                 st.write(f"**Name:** {name} | **Dept:** {emp_data.get('Department', 'N/A')}")
#
#                 st.subheader("🤖 AI Assessment")
#                 if emp_data['Performance_Trend'] == 'Pending AI Assessment':
#                     st.warning(f"**Performance Trend:** {emp_data['Performance_Trend']}")
#                 else:
#                     st.metric("Predicted Performance Trend", emp_data['Performance_Trend'])
#
#                 st.divider()
#                 st.subheader("📈 Longitudinal Performance Tracking")
#
#                 weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4 (Current)']
#                 current_task = emp_data['Task_Completion_Rate']
#                 current_eng = emp_data['Engagement_Score']
#                 current_stress = emp_data['Stress_Level'] * 10
#
#                 task_trend = [max(0, min(100, current_task + np.random.uniform(-15, 5))),
#                                   max(0, min(100, current_task + np.random.uniform(-10, 5))),
#                                   max(0, min(100, current_task + np.random.uniform(-5, 5))),
#                                   current_task]
#
#                 eng_trend = [max(0, min(100, current_eng + np.random.uniform(-10, 10))),
#                                  max(0, min(100, current_eng + np.random.uniform(-10, 10))),
#                                  max(0, min(100, current_eng + np.random.uniform(-5, 5))),
#                                  current_eng]
#
#                 stress_trend = [max(0, min(100, current_stress + np.random.uniform(-20, 20))),
#                                     max(0, min(100, current_stress + np.random.uniform(-15, 15))),
#                                     max(0, min(100, current_stress + np.random.uniform(-10, 10))),
#                                     current_stress]
#
#                 trend_df = pd.DataFrame({
#                         'Week': weeks * 3,
#                         'Score': task_trend + eng_trend + stress_trend,
#                         'Metric': ['Task Completion'] * 4 + ['Engagement'] * 4 + ['Stress Level (Scaled)'] * 4
#                     })
#
#                 fig_trend = px.line(trend_df, x='Week', y='Score', color='Metric', markers=True, title=f"4-Week Trajectory: {selected_emp}")
#                 fig_trend.update_layout(yaxis=dict(range=[0, 105]))
#                 st.plotly_chart(fig_trend, use_container_width=True)
#
#                 st.divider()
#                 st.subheader("📄 Generate Performance Report")
#                 if st.button("Generate Official PDF Report", type="primary"):
#                     with st.spinner("Generating PDF..."):
#                         pdf = FPDF()
#                         pdf.add_page()
#                         pdf.set_font("Arial", size=16, style="B")
#                         pdf.cell(200, 10, txt="Official Employee Performance Report", ln=True, align='C')
#                         pdf.ln(5)
#                         pdf.set_font("Arial", size=12, style="B")
#                         pdf.cell(200, 10, txt=f"Employee ID: {selected_emp}", ln=True)
#                         pdf.set_font("Arial", size=12)
#
#                         actual_name = emp_data.get('Employee_Name') if pd.notna(emp_data.get('Employee_Name')) else "N/A"
#                         pdf.cell(200, 10, txt=f"Name: {actual_name}", ln=True)
#                         pdf.cell(200, 10, txt=f"Department: {emp_data.get('Department', 'N/A')}", ln=True)
#                         pdf.cell(200, 10, txt=f"AI Performance Trend: {emp_data['Performance_Trend']}", ln=True)
#                         pdf.ln(5)
#
#                         pdf.set_font("Arial", size=12, style="B")
#                         pdf.cell(200, 10, txt="--- Core Metrics ---", ln=True)
#                         pdf.set_font("Arial", size=12)
#                         pdf.cell(200, 10, txt=f"Technical Score: {emp_data['Technical_Assessment_Score']}/100", ln=True)
#                         pdf.cell(200, 10, txt=f"Coding Score: {emp_data['Coding_Test_Score']}/100", ln=True)
#                         pdf.cell(200, 10, txt=f"Quiz Score: {emp_data['Average_Quiz_Score']}/100", ln=True)
#                         pdf.cell(200, 10, txt=f"Task Completion: {emp_data['Task_Completion_Rate']}%", ln=True)
#                         pdf.cell(200, 10, txt=f"Attendance Rate: {emp_data['Attendance_Rate']}%", ln=True)
#                         pdf.cell(200, 10, txt=f"Weekly Learning: {emp_data['Weekly_Learning_Hours']} Hours", ln=True)
#                         pdf.cell(200, 10, txt=f"Daily Screen Time: {emp_data['Daily_Screen_Time_Hours']} Hours", ln=True)
#                         pdf.cell(200, 10, txt=f"Stress Level: {emp_data['Stress_Level']}/10", ln=True)
#                         pdf.cell(200, 10, txt=f"Engagement Score: {emp_data['Engagement_Score']}/100", ln=True)
#                         pdf.cell(200, 10, txt=f"Mentor Feedback: {emp_data['Mentor_Feedback_Rating']}/5.0", ln=True)
#
#                         pdf_output = pdf.output(dest='S').encode('latin-1')
#                         b64 = base64.b64encode(pdf_output).decode()
#                         href = f'<br><a href="data:application/pdf;base64,{b64}" download="Report_{selected_emp}.pdf"><button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">📥 Download PDF Report</button></a>'
#                         st.markdown(href, unsafe_allow_html=True)
#
#         elif selected == "Compare Employees":
#             st.title("⚖️ Employee Comparison")
#             employee_list = st.session_state.df['Employee_ID'].tolist()
#             default_selection = employee_list[:2] if len(employee_list) >= 2 else employee_list
#             selected_emps = st.multiselect("Select Employees", employee_list, default=default_selection)
#
#             if len(selected_emps) > 0:
#                 compare_df = st.session_state.df[st.session_state.df['Employee_ID'].isin(selected_emps)]
#                 st.subheader("Skill Matrix Comparison")
#                 categories = ['Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score', 'Task_Completion_Rate', 'Attendance_Rate', 'Engagement_Score']
#                 melted_df = compare_df.melt(id_vars=['Employee_ID'], value_vars=categories, var_name='Metric', value_name='Score')
#                 fig = px.line(melted_df, x='Metric', y='Score', color='Employee_ID', markers=True, title="Skill Comparison")
#                 fig.update_layout(yaxis=dict(range=[0, 105]))
#                 st.plotly_chart(fig, use_container_width=True)
#
#         elif selected == "Remove Employee":
#             st.title("Remove Employee")
#             emp_to_remove = st.selectbox("Select Employee to Remove", sorted(st.session_state.df['Employee_ID'].tolist()))
#             if emp_to_remove and st.button("Permanently Delete", type="primary"):
#                 st.session_state.df = st.session_state.df[st.session_state.df['Employee_ID'] != emp_to_remove]
#                 save_data()
#                 st.success("Employee removed.")
#
#         elif selected == "AI Model Insights":
#             st.title("🧠 AI Model Insights & Inference Hub")
#             df_ml = pd.read_csv(FILE_NAME)
#             df_labeled = df_ml[df_ml["Performance_Trend"].isin(["Stable", "Improving", "Declining"])]
#
#             if len(df_labeled) < 10:
#                 st.info("📊 No historical data found. Generating a Synthetic Baseline to train the AI...")
#                 np.random.seed(42)
#                 n_synthetic = 5000
#                 synth_data = {
#                     'Technical_Assessment_Score': np.random.randint(40, 100, n_synthetic),
#                     'Coding_Test_Score': np.random.randint(40, 100, n_synthetic),
#                     'Average_Quiz_Score': np.random.randint(40, 100, n_synthetic),
#                     'Task_Completion_Rate': np.random.uniform(40, 100, n_synthetic),
#                     'Attendance_Rate': np.random.uniform(50, 100, n_synthetic),
#                     'Weekly_Learning_Hours': np.random.uniform(0, 20, n_synthetic),
#                     'Daily_Screen_Time_Hours': np.random.uniform(4, 12, n_synthetic),
#                     'Stress_Level': np.random.uniform(1, 10, n_synthetic),
#                     'Engagement_Score': np.random.uniform(30, 100, n_synthetic),
#                     'Mentor_Feedback_Rating': np.random.uniform(1, 5, n_synthetic)
#                 }
#                 df_labeled = pd.DataFrame(synth_data)
#
#                 def assign_trend(row):
#                     score = row['Task_Completion_Rate'] + row['Engagement_Score'] - (row['Stress_Level'] * 5)
#                     if score > 140: return "Improving"
#                     elif score < 90: return "Declining"
#                     else: return "Stable"
#
#                 df_labeled['Performance_Trend'] = df_labeled.apply(assign_trend, axis=1)
#
#             le = LabelEncoder()
#             df_labeled["Performance_Trend"] = le.fit_transform(df_labeled["Performance_Trend"])
#             x = df_labeled[['Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score', 'Task_Completion_Rate', 'Attendance_Rate', 'Weekly_Learning_Hours', 'Daily_Screen_Time_Hours', 'Stress_Level', 'Engagement_Score', 'Mentor_Feedback_Rating']]
#             y = df_labeled["Performance_Trend"]
#
#             x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
#             model = RandomForestClassifier(n_estimators=150, random_state=42)
#             model.fit(x_train, y_train)
#
#             st.success(f"**Model Trained & Ready! Accuracy:** {accuracy_score(y_test, model.predict(x_test)) * 100:.2f}%")
#
#             pending_emps = st.session_state.df[st.session_state.df['Performance_Trend'] == 'Pending AI Assessment']['Employee_ID'].tolist()
#             display_emps = pending_emps if pending_emps else reversed(st.session_state.df['Employee_ID'].tolist())
#             emp_to_predict = st.selectbox("Select Pending Employee to Evaluate (Type to search)", display_emps)
#
#             if emp_to_predict:
#                 emp_data = st.session_state.df[st.session_state.df['Employee_ID'] == emp_to_predict].iloc[0]
#
#                 if st.button("Predict Performance Trend", type="primary"):
#                     newdata = [[emp_data['Technical_Assessment_Score'], emp_data['Coding_Test_Score'], emp_data['Average_Quiz_Score'], emp_data['Task_Completion_Rate'], emp_data['Attendance_Rate'], emp_data['Weekly_Learning_Hours'], emp_data['Daily_Screen_Time_Hours'], emp_data['Stress_Level'], emp_data['Engagement_Score'], emp_data['Mentor_Feedback_Rating']]]
#                     predicted_trend = le.inverse_transform(model.predict(newdata))[0]
#
#                     st.session_state.df.loc[st.session_state.df['Employee_ID'] == emp_to_predict, 'Performance_Trend'] = predicted_trend
#                     save_data()
#
#                     if predicted_trend == "Declining":
#                         st.error(f"⚠️ Prediction: **{predicted_trend}**")
#                         st.write("- **High Stress / Low Engagement detected.** Require 1-on-1 meeting.")
#                     else:
#                         st.success(f"Prediction: **{predicted_trend}**")
#
#                 st.divider()
#                 st.subheader("🎯 Career Path Predictor (Role Recommendation)")
#                 st.write("This secondary AI model analyzes technical strengths to recommend the best-fit full-time role.")
#
#                 df_roles = pd.read_csv(FILE_NAME)
#                 df_roles = df_roles.dropna(subset=['Department'])
#
#                 if not df_roles.empty:
#                     X_role = df_roles[['Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score']]
#                     y_role = df_roles['Department']
#                     role_model = RandomForestClassifier(n_estimators=100, random_state=42)
#                     role_model.fit(X_role, y_role)
#                     role_data = [[emp_data['Technical_Assessment_Score'], emp_data['Coding_Test_Score'], emp_data['Average_Quiz_Score']]]
#                     best_fit_role = role_model.predict(role_data)[0]
#
#                     st.info(f"Based on their specific skill cluster, the AI highly recommends placing {emp_to_predict} in the **{best_fit_role}** team post-internship.")
#                 else:
#                     st.warning("Not enough Department data to train the Role Predictor yet.")
#
#     # ==========================================
#     # 🎓 INTERN PORTAL
#     # ==========================================
#     elif st.session_state.role == "Intern":
#         my_data = df[df['Employee_ID'] == st.session_state.emp_id]
#
#         if my_data.empty:
#             st.error(f"Cannot find data for {st.session_state.emp_id}. Please contact HR.")
#         else:
#             my_data = my_data.iloc[0]
#             dept = my_data.get('Department', 'N/A')
#
#             st.title(f"👋 Welcome back, {my_data.get('Employee_Name', 'Intern')}!")
#             st.markdown(f"**Department:** {dept} | **ID:** {st.session_state.emp_id}")
#
#             st.subheader("🤖 Your AI Virtual Mentor")
#             trend = my_data['Performance_Trend']
#
#             if trend == 'Pending AI Assessment':
#                 st.info("⏳ Your recent weekly data is currently being evaluated by the AI. Check back once HR runs the latest models!")
#             else:
#                 if trend in ['Stable', 'Improving']:
#                     st.success(f"**Current Trajectory:** {trend} 🚀")
#                     st.write("You are on a great path! Keep maintaining your task completion rates and engagement levels.")
#                 else:
#                     st.error(f"**Current Trajectory:** {trend} ⚠️")
#                     st.write("**Your AI-Generated Action Plan for this week:**")
#                     if my_data['Stress_Level'] >= 7.0:
#                         st.markdown("- 🧘 **Wellbeing:** Your stress metric is high. Please schedule a quick sync with your manager to balance your workload.")
#                     if my_data['Task_Completion_Rate'] < 75.0:
#                         st.markdown("- ⏱️ **Productivity:** You are falling behind on tasks. Try the Pomodoro technique: break your work into 25-minute focused sprints.")
#                     if my_data['Engagement_Score'] < 60.0:
#                         st.markdown("- 🤝 **Engagement:** Try to participate more in team stand-ups or reach out to a peer for a collaborative coding session.")
#                     if my_data['Weekly_Learning_Hours'] < 10.0:
#                         st.markdown("- 📚 **Upskilling:** Block out at least 2 hours on your calendar specifically dedicated to your learning modules.")
#
#             st.divider()
#             st.subheader("📊 Your Metrics vs. Department Average")
#
#             dept_df = df[df['Department'] == dept]
#
#             if not dept_df.empty:
#                 avg_task = dept_df['Task_Completion_Rate'].mean()
#                 avg_att = dept_df['Attendance_Rate'].mean()
#                 avg_eng = dept_df['Engagement_Score'].mean()
#
#                 c1, c2, c3, c4 = st.columns(4)
#                 c1.metric("Tech Assessment", my_data['Technical_Assessment_Score'])
#                 task_delta = my_data['Task_Completion_Rate'] - avg_task
#                 c2.metric("Task Completion", f"{my_data['Task_Completion_Rate']:.1f}%", f"{task_delta:.1f}% vs Dept")
#                 att_delta = my_data['Attendance_Rate'] - avg_att
#                 c3.metric("Attendance", f"{my_data['Attendance_Rate']:.1f}%", f"{att_delta:.1f}% vs Dept")
#                 eng_delta = my_data['Engagement_Score'] - avg_eng
#                 c4.metric("Engagement Score", f"{my_data['Engagement_Score']:.1f}", f"{eng_delta:.1f} vs Dept")
#
#                 st.divider()
#                 chart_col1, chart_col2 = st.columns(2)
#
#                 with chart_col1:
#                     st.subheader("📊 Skill Matrix Comparison")
#                     categories = ['Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score', 'Task_Completion_Rate', 'Attendance_Rate', 'Engagement_Score']
#                     intern_scores = [my_data[cat] for cat in categories]
#                     dept_scores = [dept_df[cat].mean() for cat in categories]
#                     bar_df = pd.DataFrame({
#                         'Metric': categories * 2,
#                         'Score': intern_scores + dept_scores,
#                         'Type': ['You'] * len(categories) + [f'{dept} Average'] * len(categories)
#                     })
#                     fig_bar = px.bar(bar_df, x='Metric', y='Score', color='Type', barmode='group', text_auto='.1f')
#                     fig_bar.update_layout(yaxis=dict(range=[0, 105], title="Score"), xaxis=dict(title=""), legend_title_text='')
#                     st.plotly_chart(fig_bar, use_container_width=True)
#
#                 with chart_col2:
#                     st.subheader("📈 Your 4-Week Trajectory")
#                     weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4 (Current)']
#                     current_task = my_data['Task_Completion_Rate']
#                     current_eng = my_data['Engagement_Score']
#                     current_stress = my_data['Stress_Level'] * 10
#
#                     task_trend = [max(0, min(100, current_task + np.random.uniform(-15, 5))),
#                                   max(0, min(100, current_task + np.random.uniform(-10, 5))),
#                                   max(0, min(100, current_task + np.random.uniform(-5, 5))),
#                                   current_task]
#                     eng_trend = [max(0, min(100, current_eng + np.random.uniform(-10, 10))),
#                                  max(0, min(100, current_eng + np.random.uniform(-10, 10))),
#                                  max(0, min(100, current_eng + np.random.uniform(-5, 5))),
#                                  current_eng]
#                     stress_trend = [max(0, min(100, current_stress + np.random.uniform(-20, 20))),
#                                     max(0, min(100, current_stress + np.random.uniform(-15, 15))),
#                                     max(0, min(100, current_stress + np.random.uniform(-10, 10))),
#                                     current_stress]
#
#                     trend_df = pd.DataFrame({
#                         'Week': weeks * 3,
#                         'Score': task_trend + eng_trend + stress_trend,
#                         'Metric': ['Task Completion'] * 4 + ['Engagement'] * 4 + ['Stress Level (Scaled)'] * 4
#                     })
#                     fig_line = px.line(trend_df, x='Week', y='Score', color='Metric', markers=True)
#                     fig_line.update_layout(yaxis=dict(range=[0, 105], title="Score"), xaxis=dict(title=""), legend_title_text='')
#                     st.plotly_chart(fig_line, use_container_width=True)
#
#             else:
#                 st.warning("Not enough department data to generate benchmarking yet.")
#
#     # --- LOGOUT BUTTON ---
#     with st.sidebar:
#         st.divider()
#         if st.button("🚪 Logout", use_container_width=True):
#             st.session_state.logged_in = False
#             st.rerun()