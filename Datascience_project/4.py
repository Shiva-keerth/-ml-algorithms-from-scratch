import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Workforce Readiness Predictor", layout="wide")

# --- 1. DATA INITIALIZATION & SAVING ---
FILE_NAME = "intern dataset.csv"

if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        st.error(f"Could not find '{FILE_NAME}'. Please check the file path.")
        st.stop()

df = st.session_state.df


def save_data():
    st.session_state.df.to_csv(FILE_NAME, index=False)


# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dataset","Overview", "Add New Employee", "View Employee", "Remove Employee", "AI Model Insights","Compare Employees"],
        icons=["table","bar-chart", "person-plus", "person-lines-fill", "person-x", "robot","people-fill"],
        menu_icon="briefcase",
        default_index=1  # Opened to Add Employee for testing
    )

# --- TAB 1: dataset ---
if selected == "Dataset":

    st.title("Dataset Explorer")

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isna().sum().sum())

    st.divider()

    # column selection
    selected_columns = st.multiselect(
        "Choose columns to display",
        df.columns,
        default=df.columns
    )

    filtered_df = df[selected_columns]

    # search dataset
    st.subheader("Search in Dataset")

    search_value = st.text_input("Search Any Value")

    if search_value:
        filtered_df = filtered_df[
            filtered_df.astype(str).apply(
                lambda row: row.str.contains(search_value, case=False).any(),
                axis=1
            )
        ]

    # column filter
    st.subheader("Column Filter")

    col1, col2 = st.columns(2)

    with col1:
        filter_column = st.selectbox("Select Column", filtered_df.columns)

    with col2:
        filter_value = st.selectbox(
            "Select Value",
            filtered_df[filter_column].dropna().unique()
        )

    if st.button("Apply Filter"):
        filtered_df = filtered_df[filtered_df[filter_column] == filter_value]

    st.divider()

    # row display
    st.subheader("Row display")

    rows = st.slider(
        "Number of row display",
        min_value=10,
        max_value=len(filtered_df),
        value=100
    )

    # dataset table
    st.subheader("Dataset Table")
    st.dataframe(filtered_df.head(rows), use_container_width=True)

    # show full dataset
    if st.checkbox("Show all dataset"):
        st.dataframe(df, use_container_width=True)

    st.divider()

    # columns statistics
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select Numeric Column", numeric_cols)
        st.write(filtered_df[selected_col].describe())

    st.divider()

    # download dataset
    st.subheader("Download dataset")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Dataset",
        csv,
        file_name="dataset.csv",
        mime="text/csv"
    )

if selected == "Overview":
    st.title("👥 Workforce Readiness: Strategic Talent Overview")

    total_employees = len(df)
    avg_engagement = df["Engagement_Score"].mean()
    high_risk_count = df[df["Attrition_Risk_Level"] == 'High'].shape[0]
    risk_rate = (high_risk_count / total_employees * 100) if total_employees > 0 else 0
    avg_completion = df["Task_Completion_Rate"].mean()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(label="Total Workforce", value=f"{total_employees:,}")
    kpi2.metric(label="Avg Engagement Score", value=f"{avg_engagement:.1f}/100")
    kpi3.metric(label="Critical Attrition Risk", value=f"{risk_rate:.1f}%", delta="High Risk", delta_color="inverse")
    kpi4.metric(label="Task Efficiency", value=f"{avg_completion:.1f}%")

    st.divider()

    col_trend, col_attrition = st.columns(2)

    with col_trend:
        st.subheader("Performance Trend Distribution")
        trend_dist = df["Performance_Trend"].value_counts().to_frame(name="Count")
        trend_dist["Share %"] = (trend_dist["Count"] / total_employees * 100)
        st.dataframe(trend_dist.style.format({"Share %": "{:.1f}%"}), use_container_width=True)

    with col_attrition:
        st.subheader("Attrition Risk Audit")
        attrition_dist = df["Attrition_Risk_Level"].value_counts().to_frame(name="Count")
        # Color coding: Red/Orange for risk visualization
        st.bar_chart(attrition_dist, color="#ff4b4b")


# --- TAB 2: ADD NEW EMPLOYEE ---
elif selected == "Add New Employee":
    st.title("Add New Employee")
    st.markdown(
        "Enter the employee's data below. **AI Predictions will be run separately in the AI Model Insights tab.**")

    next_id_num = len(st.session_state.df) + 1
    default_emp_id = f"EMP_{str(next_id_num).zfill(5)}"

    dept_options = st.session_state.df['Department'].dropna().unique().tolist()
    if not dept_options:
        dept_options = ["Data Analytics", "Engineering", "Marketing", "HR"]

    with st.form("add_employee_form", clear_on_submit=True):
        st.subheader("Basic Information")
        # Split into two rows for cleaner UI with the new input
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            emp_id = st.text_input("Employee ID", default_emp_id)
        with col_b:
            emp_name = st.text_input("Employee Name", "John Doe")
        with col_c:
            emp_email = st.text_input("Employee Email", "john.doe@company.com")

        col_d, col_e = st.columns(2)
        with col_d:
            emp_dept = st.selectbox("Department", dept_options)
        with col_e:
            internship_duration = st.number_input("Internship Duration (Months)", min_value=1, max_value=24, value=6)

        st.divider()

        st.subheader("Static Technical Scores")
        col1, col2, col3 = st.columns(3)
        with col1:
            tech_score = st.number_input("Technical Assessment Score (0-100)", 0, 100, 75)
        with col2:
            coding_score = st.number_input("Coding Test Score (0-100)", 0, 100, 70)
        with col3:
            quiz_score = st.number_input("Average Quiz Score (0-100)", 0, 100, 75)

        st.divider()

        st.subheader("Longitudinal Tracking (Behavioral Metrics)")
        st.write("Add a new row for each day, week, or month. The system will calculate the average.")

        default_tracking_data = pd.DataFrame({
            "Task_Completion_Rate": [85.0],
            "Mentor_Feedback_Rating": [3.8],
            "Attendance_Rate": [90.0],
            "Weekly_Learning_Hours": [15.0],
            "Daily_Screen_Time_Hours": [7.5],
            "Stress_Level": [4.5],
            "Engagement_Score": [75.0]
        })

        edited_tracking_df = st.data_editor(default_tracking_data, num_rows="dynamic", use_container_width=True)

        submitted = st.form_submit_button("Save Employee Data")

        if submitted:
            if edited_tracking_df.empty:
                st.error("Please add at least one row of tracking data.")
            else:
                task_comp = edited_tracking_df["Task_Completion_Rate"].mean()
                manager_feedback = edited_tracking_df["Mentor_Feedback_Rating"].mean()
                attendance = edited_tracking_df["Attendance_Rate"].mean()
                study_hours = edited_tracking_df["Weekly_Learning_Hours"].mean()
                screen_time = edited_tracking_df["Daily_Screen_Time_Hours"].mean()
                stress_level = edited_tracking_df["Stress_Level"].mean()
                engagement = edited_tracking_df["Engagement_Score"].mean()

                new_row = {
                    'Employee_ID': emp_id,
                    'Employee_Name': emp_name,
                    'Employee_Email': emp_email,
                    'Department': emp_dept,
                    'Company_Name': 'Pending',
                    'Role': 'New Hire',
                    'Internship_Duration_Months': internship_duration,  # SAVING THE NEW FIELD
                    'Technical_Assessment_Score': tech_score,
                    'Coding_Test_Score': coding_score,
                    'Average_Quiz_Score': quiz_score,
                    'Task_Completion_Rate': task_comp,
                    'Attendance_Rate': attendance,
                    'Weekly_Learning_Hours': study_hours,
                    'Daily_Screen_Time_Hours': screen_time,
                    'Stress_Level': stress_level,
                    'Engagement_Score': engagement,
                    'Mentor_Feedback_Rating': manager_feedback,
                    'Performance_Trend': 'Pending AI Assessment',
                    'Attrition_Risk_Level': 'Pending'
                }

                new_df = pd.DataFrame([new_row])
                st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                save_data()

                st.success(f"Employee {emp_name} ({emp_id}) added successfully! Data saved for future AI Assessment.")


# --- TAB 3: VIEW EMPLOYEE ---
elif selected == "View Employee":
    st.title("View Employee Details")

    employee_list = st.session_state.df['Employee_ID'].tolist()
    selected_emp = st.selectbox("Search / Select Employee ID", reversed(employee_list))

    if selected_emp:
        emp_data = st.session_state.df[st.session_state.df['Employee_ID'] == selected_emp].iloc[0]

        st.markdown(f"### Profile: {selected_emp}")

        name = emp_data.get('Employee_Name', 'N/A')
        email = emp_data.get('Employee_Email', 'N/A')
        dept = emp_data.get('Department', 'N/A')
        duration = emp_data.get('Internship_Duration_Months', 'N/A')  # DISPLAYING THE NEW FIELD

        st.write(f"**Name:** {name} | **Email:** {email} | **Dept:** {dept} | **Duration:** {duration} Months")

        st.subheader("🤖 AI Assessment")
        if emp_data['Performance_Trend'] == 'Pending AI Assessment':
            st.warning(f"**Performance Trend:** {emp_data['Performance_Trend']}")
        else:
            st.metric("Predicted Performance Trend", emp_data['Performance_Trend'])

        st.markdown("---")

        st.subheader("Core Metrics (Aggregated)")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Technical Assessment:** {emp_data['Technical_Assessment_Score']}")
            st.write(f"**Coding Test Score:** {emp_data['Coding_Test_Score']}")
            st.write(f"**Avg Task Completion:** {emp_data['Task_Completion_Rate']:.1f}%")
            st.write(f"**Avg Attendance:** {emp_data['Attendance_Rate']:.1f}%")
        with col2:
            st.write(f"**Avg Stress Level:** {emp_data['Stress_Level']:.1f}/10")
            st.write(f"**Avg Daily Screen Time:** {emp_data['Daily_Screen_Time_Hours']:.1f} hrs")
            st.write(f"**Avg Weekly Learning:** {emp_data['Weekly_Learning_Hours']:.1f} hrs")
            st.write(f"**Avg Mentor Feedback:** {emp_data['Mentor_Feedback_Rating']:.1f}/5.0")


# --- TAB 4: REMOVE EMPLOYEE ---
elif selected == "Remove Employee":
    st.title("Remove Employee Record")
    st.markdown("Select an employee ID from the database to permanently delete their record.")

    employee_list = st.session_state.df['Employee_ID'].tolist()
    emp_to_remove = st.selectbox("Select Employee to Remove", sorted(employee_list))

    if emp_to_remove:
        preview_data = st.session_state.df[st.session_state.df['Employee_ID'] == emp_to_remove].iloc[0]
        st.warning(
            f"You are about to delete the record for: **{emp_to_remove}** (Dept: {preview_data.get('Department', 'N/A')})")

        if st.button("Permanently Delete Employee", type="primary"):
            st.session_state.df = st.session_state.df[st.session_state.df['Employee_ID'] != emp_to_remove]
            save_data()
            st.success(f"Employee {emp_to_remove} has been removed from the dataset.")


# --- TAB 5: AI MODEL INSIGHTS (WITH PRESCRIPTIVE ANALYTICS) ---
elif selected == "AI Model Insights":
    st.title("🧠 AI Model Insights & Inference Hub")
    st.markdown("Train the Random Forest model and run predictions on pending employees.")

    st.subheader("Step 1: Train Model on Historical Data")

    df_ml = pd.read_csv(FILE_NAME)
    df_ml = df_ml[df_ml["Performance_Trend"].isin(["Stable", "Improving", "Declining"])]

    le = LabelEncoder()
    df_ml["Performance_Trend"] = le.fit_transform(df_ml["Performance_Trend"])

    x = df_ml[[
        'Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score',
        'Task_Completion_Rate', 'Attendance_Rate', 'Weekly_Learning_Hours',
        'Daily_Screen_Time_Hours', 'Stress_Level', 'Engagement_Score',
        'Mentor_Feedback_Rating'
    ]]
    y = df_ml["Performance_Trend"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=150, random_state=42)

    with st.spinner("Training Random Forest model..."):
        model.fit(x_train, y_train)

    prediction = model.predict(x_test)
    accuracy = accuracy_score(y_test, prediction)

    st.success(f"**Model Trained Successfully! Accuracy:** {accuracy * 100:.2f}%")

    st.divider()

    st.subheader("Step 2: Run Employee Assessments")
    st.write("Select an employee to evaluate their aggregated metrics and predict their performance trend.")

    pending_emps = st.session_state.df[st.session_state.df['Performance_Trend'] == 'Pending AI Assessment'][
        'Employee_ID'].tolist()
    all_emps = st.session_state.df['Employee_ID'].tolist()

    emp_to_predict = st.selectbox("Select Employee", pending_emps if pending_emps else reversed(all_emps))

    if emp_to_predict:
        emp_data = st.session_state.df[st.session_state.df['Employee_ID'] == emp_to_predict].iloc[0]
        st.write(f"**Current Status:** {emp_data['Performance_Trend']}")

        if st.button("Predict Performance Trend", type="primary"):

            newdata = [[
                emp_data['Technical_Assessment_Score'],
                emp_data['Coding_Test_Score'],
                emp_data['Average_Quiz_Score'],
                emp_data['Task_Completion_Rate'],
                emp_data['Attendance_Rate'],
                emp_data['Weekly_Learning_Hours'],
                emp_data['Daily_Screen_Time_Hours'],
                emp_data['Stress_Level'],
                emp_data['Engagement_Score'],
                emp_data['Mentor_Feedback_Rating']
            ]]

            newprediction = model.predict(newdata)
            predicted_trend = le.inverse_transform(newprediction)[0]

            st.session_state.df.loc[
                st.session_state.df['Employee_ID'] == emp_to_predict, 'Performance_Trend'] = predicted_trend
            save_data()

            if predicted_trend == "Declining":
                st.error(
                    f"⚠️ Assessment Complete! {emp_to_predict}'s Performance Trend is predicted as: **{predicted_trend}**")

                st.markdown("### 🔍 Root Cause Analysis & Improvement Plan")
                st.write(
                    "Based on the AI's analysis, here is why this employee is flagged as declining and how to help them improve.")

                col_cause, col_action = st.columns(2)

                with col_cause:
                    st.markdown("**Identified Risk Factors:**")
                    weaknesses = []
                    if emp_data['Stress_Level'] >= 6.5: weaknesses.append(
                        f"- **High Stress:** ({emp_data['Stress_Level']:.1f}/10) is a major burnout risk.")
                    if emp_data['Task_Completion_Rate'] < 75.0: weaknesses.append(
                        f"- **Low Completion:** ({emp_data['Task_Completion_Rate']:.1f}%) indicates they are falling behind.")
                    if emp_data['Attendance_Rate'] < 85.0: weaknesses.append(
                        f"- **Poor Attendance:** ({emp_data['Attendance_Rate']:.1f}%) shows disengagement.")
                    if emp_data['Engagement_Score'] < 65.0: weaknesses.append(
                        f"- **Low Engagement:** ({emp_data['Engagement_Score']:.1f}/100) indicates detachment from team goals.")
                    if emp_data['Mentor_Feedback_Rating'] < 3.5: weaknesses.append(
                        f"- **Low Mentor Rating:** ({emp_data['Mentor_Feedback_Rating']:.1f}/5) suggests a need for guidance.")
                    if emp_data['Weekly_Learning_Hours'] < 10.0: weaknesses.append(
                        f"- **Low Learning Hours:** ({emp_data['Weekly_Learning_Hours']:.1f} hrs) is stunting growth.")

                    if weaknesses:
                        for w in weaknesses: st.write(w)
                    else:
                        st.write("- General technical and behavioral scores are falling below the team baseline.")

                with col_action:
                    st.markdown("**Actionable Interventions to reach 'Stable':**")
                    if emp_data['Stress_Level'] >= 6.5: st.info(
                        "🧘 **Wellbeing:** Schedule a 1-on-1 to discuss workload balancing and mandate off-screen breaks.")
                    if emp_data['Task_Completion_Rate'] < 75.0: st.info(
                        "📊 **Productivity:** Break their current projects into smaller milestones with daily check-ins.")
                    if emp_data['Attendance_Rate'] < 85.0 or emp_data['Engagement_Score'] < 65.0: st.info(
                        "🤝 **Engagement:** Involve them in low-pressure collaborative tasks to rebuild team connection.")
                    if emp_data['Mentor_Feedback_Rating'] < 3.5 or emp_data['Weekly_Learning_Hours'] < 10.0: st.info(
                        "📚 **Mentorship:** Assign a peer buddy and block out 3 hours specifically for un-interrupted learning.")

            else:
                st.success(
                    f"Assessment Complete! {emp_to_predict}'s Performance Trend is mathematically predicted as: **{predicted_trend}**")
                st.info("The main database has been permanently updated with this prediction.")



# --- TAB 4: COMPARE EMPLOYEES ---
elif selected == "Compare Employees":
    st.title("⚖️ Employee Comparison")
    st.markdown("Select two or more employees to compare their metrics side-by-side.")

    employee_list = st.session_state.df['Employee_ID'].tolist()

    default_selection = employee_list[:2] if len(employee_list) >= 2 else employee_list
    selected_emps = st.multiselect("Select Employees to Compare", employee_list, default=default_selection)

    if len(selected_emps) > 0:
        compare_df = st.session_state.df[st.session_state.df['Employee_ID'].isin(selected_emps)]

        # --- SECTION A: VISUAL CHART ---
        st.subheader("Skill Matrix Comparison")

        categories = [
            'Technical_Assessment_Score', 'Coding_Test_Score', 'Average_Quiz_Score',
            'Task_Completion_Rate', 'Attendance_Rate', 'Engagement_Score'
        ]

        melted_df = compare_df.melt(id_vars=['Employee_ID'], value_vars=categories, var_name='Metric',
                                    value_name='Score')

        # --- THE CHART CHANGE IS HERE ---
        # To make this a Scatter Chart instead, just change 'px.line' to 'px.scatter'
        fig = px.line(
            melted_df,
            x='Metric',
            y='Score',
            color='Employee_ID',
            markers=True,  # Shows a dot at every data point
            title="Interactive Skill Comparison"
        )

        # Lock the Y-axis to 0-100 so the visual scale makes sense
        fig.update_layout(yaxis=dict(range=[0, 105]), xaxis_title="", yaxis_title="Score (out of 100)")

        # Make the scatter dots slightly larger if you switch to px.scatter
        fig.update_traces(marker=dict(size=10))

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- SECTION B: SIDE-BY-SIDE DATA TABLE ---
        st.subheader("Head-to-Head Data Table")

        display_cols = [
            'Employee_ID', 'Department', 'Performance_Trend', 'Attrition_Risk_Level',
            'Technical_Assessment_Score', 'Task_Completion_Rate', 'Stress_Level', 'Mentor_Feedback_Rating'
        ]

        table_df = compare_df[display_cols].set_index('Employee_ID').T

        st.dataframe(table_df, use_container_width=True)

    else:
        st.info("Please select at least one employee from the dropdown above to view the comparison.")