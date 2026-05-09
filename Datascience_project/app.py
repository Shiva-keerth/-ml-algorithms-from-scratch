import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import smtplib
import random
import hashlib
from email.mime.text import MIMEText
from fpdf import FPDF
import base64
import time
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Workforce Readiness Platform", layout="wide")

# ==========================================
# 🎨 EMBEDDED PREMIUM UI CSS (FIXED & SAFE)
# ==========================================
CUSTOM_CSS = """
<style>
/* Hide default header/footer safely */
[data-testid="stHeader"] {visibility: hidden;}
footer {visibility: hidden;}

/* Safe Background Gradient */
.stApp {
    background: linear-gradient(135deg, #0f121b 0%, #171c2b 100%);
    color: #ffffff;
}

/* Animated Blobs - Fixed positioning and pointer-events:none prevents blocking UI */
.stApp::before {
    content: "";
    position: fixed;
    top: -10%; left: -10%;
    width: 50vw; height: 50vh;
    background: radial-gradient(circle, rgba(76, 175, 80, 0.12) 0%, rgba(0,0,0,0) 70%);
    animation: floatBlob 15s infinite alternate ease-in-out;
    z-index: 0;
    pointer-events: none; 
}

.stApp::after {
    content: "";
    position: fixed;
    bottom: -10%; right: -10%;
    width: 60vw; height: 60vh;
    background: radial-gradient(circle, rgba(63, 81, 181, 0.12) 0%, rgba(0,0,0,0) 70%);
    animation: floatBlob2 20s infinite alternate ease-in-out;
    z-index: 0;
    pointer-events: none;
}

/* Ensure the actual app content stays above the animated background */
[data-testid="stAppViewBlockContainer"] {
    position: relative;
    z-index: 1;
}

@keyframes floatBlob {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(100px, 100px) scale(1.2); }
}

@keyframes floatBlob2 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(-100px, -150px) scale(1.1); }
}

/* Glassmorphism Cards */
[data-testid="stMetric"], [data-testid="stForm"], [data-testid="stExpander"] {
    background: rgba(30, 34, 53, 0.4) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255,255,255,0.05);
    transition: transform 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(76, 175, 80, 0.3);
}

[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
}

/* Custom Inputs & Buttons */
.stTextInput > div > div > input {
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.1) !important;
    background-color: rgba(0,0,0,0.3) !important;
    color: white !important;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border: 1px solid #4CAF50 !important;
    box-shadow: 0 0 10px rgba(76, 175, 80, 0.3) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(76, 175, 80, 0.4) !important;
}

/* Sidebar Glassmorphism */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(255,255,255,0.05);
    background: rgba(14, 17, 23, 0.8) !important;
    backdrop-filter: blur(20px) !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================
# ⚙️ CONFIGURATION & HELPER FUNCTIONS
# ==========================================
def load_lottieurl(url: str):
    try:
        # Added a 5-second timeout so it doesn't hang the app!
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


def stream_typing_effect(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.04)


SENDER_EMAIL = "your_email@gmail.com"
EMAIL_AUTH_VAR = "your_sixteen_digit_app_str"

USER_FILE = "users.csv"
FILE_NAME = "intern dataset.csv"


def init_db():
    try:
        pd.read_csv(USER_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Email", "Password", "Role", "Employee_ID"])
        df.to_csv(USER_FILE, index=False)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def send_otp_email(receiver_email, otp):
    try:
        msg = MIMEText(f"Your Workforce Portal verification code is: {otp}")
        msg['Subject'] = 'Portal Registration OTP'
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [receiver_email], msg.as_string())
        server.quit()
        return True
    except Exception:
        print(f"\n⚠️ EMAIL FAILED. Developer Mode OTP for {receiver_email} is: {otp}\n")
        return False


def save_data():
    st.session_state.df.to_csv(FILE_NAME, index=False)


init_db()
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "otp" not in st.session_state: st.session_state.otp = None
if "register_data" not in st.session_state: st.session_state.register_data = None

# ==========================================
# 🛑 UNAUTHENTICATED VIEW (LOGIN/REGISTER)
# ==========================================
if not st.session_state.logged_in:
    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        lottie_login = load_lottieurl("https://lottie.host/880b957e-dbdf-43e6-bf25-46a4da90635f/tXq8v6KXY8.json")
        if lottie_login:
            st_lottie(lottie_login, height=150, key="login_anim")

        st.title("🔐 Workforce Portal")
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            login_email = st.text_input("Email", key="login_email")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", type="primary", use_container_width=True):
                users_df = pd.read_csv(USER_FILE)
                hashed_input = hash_password(login_pass)
                user = users_df[(users_df['Email'] == login_email) & (users_df['Password'] == hashed_input)]

                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.role = user.iloc[0]['Role']
                    st.session_state.user_email = user.iloc[0]['Email']
                    st.session_state.emp_id = user.iloc[0]['Employee_ID']
                    st.rerun()
                else:
                    st.error("Invalid Email or Password")

        with tab2:
            reg_email = st.text_input("Work Email")
            reg_pass = st.text_input("Password", type="password")
            reg_role = st.selectbox("Register as:", ["Intern", "HR"])

            reg_emp_id = "N/A"
            if reg_role == "Intern":
                reg_emp_id = st.text_input("Your Employee ID (e.g., EMP_00001)")

            if st.button("Send Verification Code", use_container_width=True):
                users_df = pd.read_csv(USER_FILE)
                if reg_email in users_df['Email'].values:
                    st.error("Email is already registered!")
                elif reg_role == "Intern" and not reg_emp_id:
                    st.error("Interns must provide their Employee ID.")
                else:
                    st.session_state.otp = str(random.randint(100000, 999999))
                    st.session_state.register_data = {
                        "Email": reg_email, "Password": hash_password(reg_pass),
                        "Role": reg_role, "Employee_ID": reg_emp_id
                    }
                    if send_otp_email(reg_email, st.session_state.otp):
                        st.success("OTP sent to your email!")
                    else:
                        st.warning("Check your terminal for the OTP!")

            if st.session_state.otp:
                entered_otp = st.text_input("Enter 6-digit OTP", max_chars=6)
                if st.button("Verify & Register", type="primary"):
                    if entered_otp == st.session_state.otp:
                        new_user = pd.DataFrame([st.session_state.register_data])
                        new_user.to_csv(USER_FILE, mode='a', header=False, index=False)
                        st.success("Account created! You can now Login.")
                        st.session_state.otp = None
                    else:
                        st.error("Incorrect OTP.")

# ==========================================
# ✅ AUTHENTICATED VIEW (THE PLATFORM)
# ==========================================
else:
    if 'df' not in st.session_state:
        try:
            st.session_state.df = pd.read_csv(FILE_NAME)
        except FileNotFoundError:
            st.error(f"Cannot find {FILE_NAME}")
            st.stop()

    df = st.session_state.df

    with st.sidebar:
        st.markdown(f"### 👤 Profile")
        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Role:** {st.session_state.role}")
        if st.session_state.role == "Intern":
            st.write(f"**ID:** {st.session_state.emp_id}")
        st.divider()

    # ==========================================
    # 👨‍💼 HR PORTAL
    # ==========================================
    if st.session_state.role == "HR":
        with st.sidebar:
            selected = option_menu(
                "HR Menu",
                ["Overview", "Add New Employee", "View Employee", "Compare Employees", "Remove Employee",
                 "AI Model Insights"],
                icons=["bar-chart", "person-plus", "person-lines-fill", "people-fill", "person-x", "robot"],
                default_index=0
            )

        if selected == "Overview":
            st.title("👥 Workforce Readiness: Strategic Talent Overview")
            total_employees = len(df)
            avg_engagement = df["Engagement_Score"].mean()
            high_risk_count = df[df["Attrition_Risk_Level"] == 'High'].shape[
                0] if "Attrition_Risk_Level" in df.columns else 0
            risk_rate = (high_risk_count / total_employees * 100) if total_employees > 0 else 0
            avg_completion = df["Task_Completion_Rate"].mean()

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Total Workforce", f"{total_employees:,}")
            kpi2.metric("Avg Engagement", f"{avg_engagement:.1f}/100")
            kpi3.metric("Critical Attrition Risk", f"{risk_rate:.1f}%", delta="High Risk", delta_color="inverse")
            kpi4.metric("Task Efficiency", f"{avg_completion:.1f}%")

            st.divider()
            col_trend, col_attrition = st.columns(2)
            with col_trend:
                st.subheader("Performance Trend Distribution")
                trend_dist = df["Performance_Trend"].value_counts().to_frame(name="Count")
                trend_dist["Share %"] = (trend_dist["Count"] / total_employees * 100)
                st.dataframe(trend_dist.style.format({"Share %": "{:.1f}%"}), use_container_width=True)
            with col_attrition:
                st.subheader("Attrition Risk Audit")
                if "Attrition_Risk_Level" in df.columns:
                    attrition_dist = df["Attrition_Risk_Level"].value_counts().to_frame(name="Count")
                    st.bar_chart(attrition_dist, color="#ff4b4b")

        elif selected == "Add New Employee":
            st.title("Add New Employee")
            st.markdown(
                "Enter the static day-one details below. **The RPA Bot will automatically track their weekly metrics!**")

            next_id_num = len(st.session_state.df) + 1
            default_emp_id = f"EMP_{str(next_id_num).zfill(5)}"
            dept_options = st.session_state.df['Department'].dropna().unique().tolist()
            if not dept_options: dept_options = ["Data Analytics", "Engineering", "HR"]

            with st.form("add_employee_form", clear_on_submit=True):
                st.subheader("Basic Information")
                col_a, col_b, col_c = st.columns(3)
                with col_a: emp_id = st.text_input("Employee ID", default_emp_id)
                with col_b: emp_name = st.text_input("Employee Name", "John Doe")
                with col_c: emp_email = st.text_input("Employee Email", "john.doe@company.com")

                col_d, col_e = st.columns(2)
                with col_d: emp_dept = st.selectbox("Department", dept_options)
                with col_e: internship_duration = st.number_input("Internship Duration (Months)", 1, 24, 6)

                st.divider()
                st.subheader("Static Technical Scores (Day 1)")
                col1, col2, col3 = st.columns(3)
                with col1: tech_score = st.number_input("Tech Assessment (0-100)", 0, 100, 75)
                with col2: coding_score = st.number_input("Coding Test (0-100)", 0, 100, 70)
                with col3: quiz_score = st.number_input("Initial Quiz Score (0-100)", 0, 100, 75)

                st.divider()
                st.info(
                    "🤖 **Automation Active:** Weekly tracking metrics will be automatically populated by the RPA Bot.")

                if st.form_submit_button("Save Employee Data"):
                    new_row = {
                        'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Employee_Email': emp_email,
                        'Department': emp_dept, 'Company_Name': 'Pending', 'Role': 'New Hire',
                        'Internship_Duration_Months': internship_duration, 'Technical_Assessment_Score': tech_score,
                        'Coding_Test_Score': coding_score, 'Average_Quiz_Score': quiz_score,
                        'Task_Completion_Rate': 0.0, 'Attendance_Rate': 0.0, 'Weekly_Learning_Hours': 0.0,
                        'Daily_Screen_Time_Hours': 0.0, 'Stress_Level': 0.0, 'Engagement_Score': 0.0,
                        'Mentor_Feedback_Rating': 0.0, 'Performance_Trend': 'Pending AI Assessment',
                        'Attrition_Risk_Level': 'Pending'
                    }
                    new_df = pd.DataFrame([new_row])
                    st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                    save_data()
                    st.success(f"Employee {emp_name} added successfully!")

        elif selected == "View Employee":
            st.title("View Employee Details")
            employee_list = st.session_state.df['Employee_ID'].tolist()

            # FIX 1: Wrapped reversed in a list() to fix the crash
            selected_emp = st.selectbox("Select Employee", list(reversed(employee_list)))

            if selected_emp:
                emp_data = st.session_state.df[st.session_state.df['Employee_ID'] == selected_emp].iloc[0]
                st.markdown(f"### Profile: {selected_emp}")
                name = emp_data.get('Employee_Name', 'N/A')
                st.write(f"**Name:** {name} | **Dept:** {emp_data.get('Department', 'N/A')}")

                st.subheader("🤖 AI Assessment")
                if emp_data['Performance_Trend'] == 'Pending AI Assessment':
                    st.warning(f"**Performance Trend:** {emp_data['Performance_Trend']}")
                else:
                    st.metric("Predicted Performance Trend", emp_data['Performance_Trend'])

                st.divider()
                st.subheader("📈 Longitudinal Performance Tracking")

                weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4 (Current)']
                current_task = emp_data['Task_Completion_Rate']
                current_eng = emp_data['Engagement_Score']
                current_stress = emp_data['Stress_Level'] * 10

                # FIX 2: Seed the random generator using Employee ID to stop UI jumping
                seed_val = int(hashlib.md5(selected_emp.encode()).hexdigest(), 16) % (10 ** 8)
                np.random.seed(seed_val)

                task_trend = [max(0, min(100, current_task + np.random.uniform(-15, 5))),
                              max(0, min(100, current_task + np.random.uniform(-10, 5))),
                              max(0, min(100, current_task + np.random.uniform(-5, 5))),
                              current_task]

                eng_trend = [max(0, min(100, current_eng + np.random.uniform(-10, 10))),
                             max(0, min(100, current_eng + np.random.uniform(-10, 10))),
                             max(0, min(100, current_eng + np.random.uniform(-5, 5))),
                             current_eng]

                stress_trend = [max(0, min(100, current_stress + np.random.uniform(-20, 20))),
                                max(0, min(100, current_stress + np.random.uniform(-15, 15))),
                                max(0, min(100, current_stress + np.random.uniform(-10, 10))),
                                current_stress]

                trend_df = pd.DataFrame({
                    'Week': weeks * 3,
                    'Score': task_trend + eng_trend + stress_trend,
                    'Metric': ['Task Completion'] * 4 + ['Engagement'] * 4 + ['Stress Level (Scaled)'] * 4
                })

                fig_trend = px.line(trend_df, x='Week', y='Score', color='Metric', markers=True,
                                    title=f"4-Week Trajectory: {selected_emp}")
                fig_trend.update_layout(yaxis=dict(range=[0, 105]), paper_bgcolor="rgba(0,0,0,0)",
                                        plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig_trend, use_container_width=True)

                st.divider()
                st.subheader("📄 Generate Performance Report")
                if st.button("Generate Official PDF Report", type="primary"):
                    with st.spinner("Generating Premium PDF..."):
                        pdf = FPDF()
                        pdf.add_page()

                        # --- 1. PREMIUM DARK HEADER ---
                        pdf.set_fill_color(23, 28, 43)  # Matches your app's dark blue/black background
                        pdf.rect(0, 0, 210, 40, 'F')

                        pdf.set_y(15)
                        pdf.set_font("Arial", size=22, style="B")
                        pdf.set_text_color(255, 255, 255)  # White text
                        pdf.cell(200, 10, txt="WORKFORCE AI INSIGHTS REPORT", ln=True, align='C')

                        # --- 2. EMPLOYEE PROFILE SECTION ---
                        pdf.set_y(50)
                        pdf.set_text_color(44, 62, 80)  # Dark Slate Gray
                        pdf.set_font("Arial", size=14, style="B")
                        pdf.cell(200, 10, txt="EMPLOYEE PROFILE", ln=True, align='L')

                        # Divider Line
                        pdf.set_draw_color(200, 200, 200)
                        pdf.line(10, 60, 200, 60)
                        pdf.ln(5)

                        pdf.set_font("Arial", size=11)
                        actual_name = emp_data.get('Employee_Name', 'N/A')

                        # Side-by-side profile info
                        pdf.cell(100, 8, txt=f"Name: {actual_name}", ln=False)
                        pdf.cell(100, 8, txt=f"Employee ID: {selected_emp}", ln=True)
                        pdf.cell(100, 8, txt=f"Department: {emp_data.get('Department', 'N/A')}", ln=True)
                        pdf.ln(5)

                        # --- 3. COLOR-CODED AI HIGHLIGHT BOX ---
                        # Light gray background for the highlight box
                        pdf.set_fill_color(245, 247, 250)
                        pdf.rect(10, pdf.get_y(), 190, 25, 'F')

                        pdf.set_y(pdf.get_y() + 5)
                        pdf.set_font("Arial", size=12, style="B")
                        pdf.cell(70, 8, txt="  AI Performance Prediction:", ln=False)

                        # Color code the trend text
                        trend_val = emp_data['Performance_Trend']
                        if trend_val == 'Improving':
                            pdf.set_text_color(39, 174, 96)  # Green
                        elif trend_val == 'Declining':
                            pdf.set_text_color(231, 76, 60)  # Red
                        else:
                            pdf.set_text_color(41, 128, 185)  # Blue

                        pdf.set_font("Arial", size=14, style="B")
                        pdf.cell(100, 8, txt=f"{trend_val.upper()}", ln=True)
                        pdf.set_text_color(44, 62, 80)  # Reset text color to slate
                        pdf.ln(10)

                        # --- 4. CORE METRICS GRID ---
                        pdf.set_font("Arial", size=14, style="B")
                        pdf.cell(200, 10, txt="CORE METRICS & TRACKING", ln=True, align='L')
                        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                        pdf.ln(5)


                        # Helper function to make rows look like a clean table
                        def pdf_metric_row(label, value):
                            pdf.set_font("Arial", size=11, style="B")
                            pdf.cell(70, 8, txt=label, ln=False)
                            pdf.set_font("Arial", size=11)
                            pdf.cell(100, 8, txt=str(value), ln=True)


                        pdf_metric_row("Technical Score:", f"{emp_data['Technical_Assessment_Score']}/100")
                        pdf_metric_row("Coding Score:", f"{emp_data['Coding_Test_Score']}/100")
                        pdf_metric_row("Quiz Score:", f"{emp_data['Average_Quiz_Score']}/100")
                        pdf_metric_row("Task Completion Rate:", f"{emp_data['Task_Completion_Rate']}%")
                        pdf_metric_row("Attendance Rate:", f"{emp_data['Attendance_Rate']}%")
                        pdf_metric_row("Weekly Learning:", f"{emp_data['Weekly_Learning_Hours']} Hours")
                        pdf_metric_row("Daily Screen Time:", f"{emp_data['Daily_Screen_Time_Hours']} Hours")
                        pdf_metric_row("Stress Level:", f"{emp_data['Stress_Level']}/10")
                        pdf_metric_row("Engagement Score:", f"{emp_data['Engagement_Score']}/100")
                        pdf_metric_row("Mentor Feedback:", f"{emp_data['Mentor_Feedback_Rating']}/5.0")

                        # --- 5. PROFESSIONAL FOOTER ---
                        pdf.set_y(260)  # Push to the bottom of the page
                        pdf.set_font("Arial", size=9, style="I")
                        pdf.set_text_color(150, 150, 150)
                        pdf.cell(0, 10, "Generated autonomously by Workforce Readiness Platform AI", 0, 0, 'C')

                        # --- GENERATE AND DOWNLOAD ---
                        pdf_output = pdf.output(dest='S').encode('latin-1')
                        b64 = base64.b64encode(pdf_output).decode()
                        href = f'<br><a href="data:application/pdf;base64,{b64}" download="Report_{selected_emp}.pdf"><button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📥 Download Premium PDF Report</button></a>'
                        st.markdown(href, unsafe_allow_html=True)
        elif selected == "Compare Employees":
            st.title("⚖️ Employee Comparison")
            employee_list = st.session_state.df['Employee_ID'].tolist()
            default_selection = employee_list[:2] if len(employee_list) >= 2 else employee_list
            selected_emps = st.multiselect("Select Employees", employee_list, default=default_selection)

            if len(selected_emps) > 0:
                compare_df = st.session_state.df[st.session_state.df['Employee_ID'].isin(selected_emps)]
                st.subheader("Skill Matrix Comparison")
                categories = ['Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score',
                              'Task_Completion_Rate', 'Attendance_Rate', 'Engagement_Score']
                melted_df = compare_df.melt(id_vars=['Employee_ID'], value_vars=categories, var_name='Metric',
                                            value_name='Score')
                fig = px.line(melted_df, x='Metric', y='Score', color='Employee_ID', markers=True,
                              title="Skill Comparison")
                fig.update_layout(yaxis=dict(range=[0, 105]), paper_bgcolor="rgba(0,0,0,0)",
                                  plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)

        elif selected == "Remove Employee":
            st.title("Remove Employee")
            emp_to_remove = st.selectbox("Select Employee to Remove",
                                         sorted(st.session_state.df['Employee_ID'].tolist()))
            if emp_to_remove and st.button("Permanently Delete", type="primary"):
                st.session_state.df = st.session_state.df[st.session_state.df['Employee_ID'] != emp_to_remove]
                save_data()
                st.success("Employee removed.")

        elif selected == "AI Model Insights":
            st.title("🧠 AI Model Insights & Inference Hub")
            df_ml = pd.read_csv(FILE_NAME)
            df_labeled = df_ml[df_ml["Performance_Trend"].isin(["Stable", "Improving", "Declining"])]

            if len(df_labeled) < 10:
                st.info("📊 No historical data found. Generating a Synthetic Baseline to train the AI...")
                np.random.seed(42)
                n_synthetic = 5000
                synth_data = {
                    'Technical_Assessment_Score': np.random.randint(40, 100, n_synthetic),
                    'Coding_Test_Score': np.random.randint(40, 100, n_synthetic),
                    'Average_Quiz_Score': np.random.randint(40, 100, n_synthetic),
                    'Task_Completion_Rate': np.random.uniform(40, 100, n_synthetic),
                    'Attendance_Rate': np.random.uniform(50, 100, n_synthetic),
                    'Weekly_Learning_Hours': np.random.uniform(0, 20, n_synthetic),
                    'Daily_Screen_Time_Hours': np.random.uniform(4, 12, n_synthetic),
                    'Stress_Level': np.random.uniform(1, 10, n_synthetic),
                    'Engagement_Score': np.random.uniform(30, 100, n_synthetic),
                    'Mentor_Feedback_Rating': np.random.uniform(1, 5, n_synthetic)
                }
                df_labeled = pd.DataFrame(synth_data)


                def assign_trend(row):
                    score = row['Task_Completion_Rate'] + row['Engagement_Score'] - (row['Stress_Level'] * 5)
                    if score > 140:
                        return "Improving"
                    elif score < 90:
                        return "Declining"
                    else:
                        return "Stable"


                df_labeled['Performance_Trend'] = df_labeled.apply(assign_trend, axis=1)

            le = LabelEncoder()
            df_labeled["Performance_Trend"] = le.fit_transform(df_labeled["Performance_Trend"])
            x = df_labeled[
                ['Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score', 'Task_Completion_Rate',
                 'Attendance_Rate', 'Weekly_Learning_Hours', 'Daily_Screen_Time_Hours', 'Stress_Level',
                 'Engagement_Score', 'Mentor_Feedback_Rating']]
            y = df_labeled["Performance_Trend"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
            model = RandomForestClassifier(n_estimators=150, random_state=42)
            model.fit(x_train, y_train)

            st.success(
                f"**Model Trained & Ready! Accuracy:** {accuracy_score(y_test, model.predict(x_test)) * 100:.2f}%")

            pending_emps = st.session_state.df[st.session_state.df['Performance_Trend'] == 'Pending AI Assessment'][
                'Employee_ID'].tolist()

            # FIX 1 (Continued): Wrap reversed in a list() to fix the crash
            display_emps = pending_emps if pending_emps else list(reversed(st.session_state.df['Employee_ID'].tolist()))
            emp_to_predict = st.selectbox("Select Pending Employee to Evaluate (Type to search)", display_emps)

            # --- BULLETPROOF FIX: Safely checks if an employee is actually selected first ---
            if emp_to_predict is not None and len(emp_to_predict) > 0:
                emp_data = st.session_state.df[st.session_state.df['Employee_ID'] == emp_to_predict].iloc[0]

                if st.button("Predict Performance Trend", type="primary"):
                    newdata = [[emp_data['Technical_Assessment_Score'], emp_data['Coding_Test_Score'],
                                emp_data['Average_Quiz_Score'], emp_data['Task_Completion_Rate'],
                                emp_data['Attendance_Rate'], emp_data['Weekly_Learning_Hours'],
                                emp_data['Daily_Screen_Time_Hours'], emp_data['Stress_Level'],
                                emp_data['Engagement_Score'], emp_data['Mentor_Feedback_Rating']]]
                    predicted_trend = le.inverse_transform(model.predict(newdata))[0]

                    st.session_state.df.loc[
                        st.session_state.df['Employee_ID'] == emp_to_predict, 'Performance_Trend'] = predicted_trend
                    save_data()

                    if predicted_trend == "Declining":
                        st.error(f"⚠️ Prediction: **{predicted_trend}**")
                        st.write("- **High Stress / Low Engagement detected.** Require 1-on-1 meeting.")
                    else:
                        st.success(f"Prediction: **{predicted_trend}**")

                st.divider()
                st.subheader("🎯 Career Path Predictor (Role Recommendation)")
                st.write(
                    "This secondary AI model analyzes technical strengths to recommend the best-fit full-time role.")

                df_roles = pd.read_csv(FILE_NAME)
                df_roles = df_roles.dropna(subset=['Department'])

                if not df_roles.empty:
                    X_role = df_roles[['Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score']]
                    y_role = df_roles['Department']
                    role_model = RandomForestClassifier(n_estimators=100, random_state=42)
                    role_model.fit(X_role, y_role)

                    role_data = [[emp_data['Technical_Assessment_Score'], emp_data['Coding_Test_Score'],
                                  emp_data['Average_Quiz_Score']]]
                    best_fit_role = role_model.predict(role_data)[0]

                    st.info(
                        f"Based on their specific skill cluster, the AI highly recommends placing {emp_to_predict} in the **{best_fit_role}** team post-internship.")
                else:
                    st.warning("Not enough Department data to train the Role Predictor yet.")
            else:
                st.info("Please select an employee above to view their AI insights.")

    # ==========================================
    # 🎓 INTERN PORTAL (Massive UI Upgrade)
    # ==========================================
    elif st.session_state.role == "Intern":
        my_data = df[df['Employee_ID'] == st.session_state.emp_id]

        if my_data.empty:
            st.error(f"Cannot find data for {st.session_state.emp_id}. Please contact HR.")
        else:
            my_data = my_data.iloc[0]
            dept = my_data.get('Department', 'N/A')

            st.title(f"👋 Welcome back, {my_data.get('Employee_Name', 'Intern')}!")
            st.markdown(f"**Department:** {dept} | **ID:** {st.session_state.emp_id}")

            st.divider()
            ment_col1, ment_col2 = st.columns([1, 3])

            with ment_col1:
                lottie_robot = load_lottieurl(
                    "https://lottie.host/21191060-8456-42d8-bf11-7393e1104eab/lQfXU4JtZ8.json")
                if lottie_robot:
                    st_lottie(lottie_robot, height=200, key="robot")

            with ment_col2:
                st.subheader("🤖 Your AI Virtual Mentor")
                trend = my_data['Performance_Trend']

                if trend == 'Pending AI Assessment':
                    st.info(
                        "⏳ Your recent weekly data is currently being evaluated by the AI. Check back once HR runs the latest models!")
                else:
                    if trend in ['Stable', 'Improving']:
                        st.success(f"**Current Trajectory:** {trend} 🚀")
                        st.write_stream(stream_typing_effect(
                            "You are on a great path! Keep maintaining your task completion rates and engagement levels."))
                    else:
                        st.error(f"**Current Trajectory:** {trend} ⚠️")
                        st.write("**Your AI-Generated Action Plan for this week:**")

                        action_plan = ""
                        if my_data['Stress_Level'] >= 7.0:
                            action_plan += "- 🧘 **Wellbeing:** Your stress metric is high. Please schedule a quick sync with your manager.\n"
                        if my_data['Task_Completion_Rate'] < 75.0:
                            action_plan += "- ⏱️ **Productivity:** You are falling behind on tasks. Try the Pomodoro technique (25-minute focused sprints).\n"
                        if my_data['Engagement_Score'] < 60.0:
                            action_plan += "- 🤝 **Engagement:** Try to participate more in team stand-ups or reach out to a peer for a collaborative session.\n"
                        if my_data['Weekly_Learning_Hours'] < 10.0:
                            action_plan += "- 📚 **Upskilling:** Block out at least 2 hours on your calendar specifically dedicated to your learning modules.\n"

                        if action_plan:
                            st.write_stream(stream_typing_effect(action_plan))

            st.divider()
            st.subheader("📊 Performance Rings (vs Dept Average)")

            dept_df = df[df['Department'] == dept]

            if not dept_df.empty:
                avg_task = dept_df['Task_Completion_Rate'].mean()
                avg_att = dept_df['Attendance_Rate'].mean()
                avg_eng = dept_df['Engagement_Score'].mean()

                ring_c1, ring_c2, ring_c3 = st.columns(3)


                def create_gauge(title, value, reference, color):
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=value,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': title, 'font': {'size': 18, 'color': 'white'}},
                        delta={'reference': reference, 'increasing': {'color': "#4CAF50"},
                               'decreasing': {'color': "#FF5252"}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                            'bar': {'color': color},
                            'bgcolor': "rgba(0,0,0,0)",
                            'borderwidth': 2,
                            'bordercolor': "rgba(255,255,255,0.2)",
                            'steps': [
                                {'range': [0, 50], 'color': "rgba(255,255,255,0.05)"},
                                {'range': [50, 80], 'color': "rgba(255,255,255,0.1)"}],
                        }
                    ))
                    fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)",
                                      font={'color': "white"})
                    return fig


                with ring_c1:
                    st.plotly_chart(
                        create_gauge("Task Completion", my_data['Task_Completion_Rate'], avg_task, "#4CAF50"),
                        use_container_width=True)
                with ring_c2:
                    st.plotly_chart(create_gauge("Attendance", my_data['Attendance_Rate'], avg_att, "#2196F3"),
                                    use_container_width=True)
                with ring_c3:
                    st.plotly_chart(create_gauge("Engagement", my_data['Engagement_Score'], avg_eng, "#9C27B0"),
                                    use_container_width=True)

                st.divider()
                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    st.subheader("📊 Skill Matrix Comparison")
                    categories = ['Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score',
                                  'Task_Completion_Rate', 'Attendance_Rate', 'Engagement_Score']
                    intern_scores = [my_data[cat] for cat in categories]
                    dept_scores = [dept_df[cat].mean() for cat in categories]
                    bar_df = pd.DataFrame({
                        'Metric': categories * 2,
                        'Score': intern_scores + dept_scores,
                        'Type': ['You'] * len(categories) + [f'{dept} Average'] * len(categories)
                    })
                    fig_bar = px.bar(bar_df, x='Metric', y='Score', color='Type', barmode='group', text_auto='.1f')
                    fig_bar.update_layout(yaxis=dict(range=[0, 105], title="Score"), xaxis=dict(title=""),
                                          legend_title_text='', paper_bgcolor="rgba(0,0,0,0)",
                                          plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig_bar, use_container_width=True)

                with chart_col2:
                    st.subheader("📈 Your 4-Week Trajectory")
                    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4 (Current)']
                    current_task = my_data['Task_Completion_Rate']
                    current_eng = my_data['Engagement_Score']
                    current_stress = my_data['Stress_Level'] * 10

                    # FIX 2 (Continued): Seed the random generator using Intern's Employee ID
                    seed_val = int(hashlib.md5(st.session_state.emp_id.encode()).hexdigest(), 16) % (10 ** 8)
                    np.random.seed(seed_val)

                    task_trend = [max(0, min(100, current_task + np.random.uniform(-15, 5))),
                                  max(0, min(100, current_task + np.random.uniform(-10, 5))),
                                  max(0, min(100, current_task + np.random.uniform(-5, 5))),
                                  current_task]
                    eng_trend = [max(0, min(100, current_eng + np.random.uniform(-10, 10))),
                                 max(0, min(100, current_eng + np.random.uniform(-10, 10))),
                                 max(0, min(100, current_eng + np.random.uniform(-5, 5))),
                                 current_eng]
                    stress_trend = [max(0, min(100, current_stress + np.random.uniform(-20, 20))),
                                    max(0, min(100, current_stress + np.random.uniform(-15, 15))),
                                    max(0, min(100, current_stress + np.random.uniform(-10, 10))),
                                    current_stress]

                    trend_df = pd.DataFrame({
                        'Week': weeks * 3,
                        'Score': task_trend + eng_trend + stress_trend,
                        'Metric': ['Task Completion'] * 4 + ['Engagement'] * 4 + ['Stress Level (Scaled)'] * 4
                    })
                    fig_line = px.line(trend_df, x='Week', y='Score', color='Metric', markers=True)
                    fig_line.update_layout(yaxis=dict(range=[0, 105], title="Score"), xaxis=dict(title=""),
                                           legend_title_text='', paper_bgcolor="rgba(0,0,0,0)",
                                           plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig_line, use_container_width=True)

            else:
                st.warning("Not enough department data to generate benchmarking yet.")

    # --- LOGOUT BUTTON ---
    with st.sidebar:
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()