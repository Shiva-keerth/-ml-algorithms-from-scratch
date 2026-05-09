import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Student Performance Management System",layout="wide")
st.title("Student Performance Management System")

if "student" not in st.session_state:
    st.session_state.student=[]

if "last_action" not in st.session_state:
    st.session_state.last_action="System started"

st.subheader("Add Records")

col1,col2,col3,col4 =st.columns(4)

with col1:
    name=st.text_input("Student Name")
with col2:
    roll_no=st.text_input("Roll No")
with col3:
    subjects=st.selectbox("Subjects",["Math","Science","English","Computer"])
with col4:
    marks=st.number_input("Marks",min_value=0,max_value=100,step=1)

if st.button("Add Record"):
    name=name.strip()
    roll_no=roll_no.strip()
    if name and roll_no:
        records ={
            "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name":name.strip(),
            "roll_no":roll_no.strip(),
            "subjects":subjects,
            "marks":marks
        }
        duplicate_found=False
        for existing in st.session_state.student:
            if existing["roll_no"] == roll_no and existing["subjects"] == subjects:
                duplicate_found=True
                break
        if duplicate_found:
            st.warning("This roll already has marks for this subject")
        else:
              st.session_state.student.append(records)
              st.session_state.last_action = "Added record for "+name
              st.success("Record added successfully")

# filter record

st.subheader("Filter Records")
filter1=st.selectbox("Filter Records",["All","Math", "Science", "English", "Computer"])
filtered_records=[]
if filter1 == "All":
    filtered_records=st.session_state.student
else:
    for r in st.session_state.student:
        if r["subjects"] == filter1:
            filtered_records.append(r)

# display part
st.subheader("Students records")
if not filtered_records:
    st.info("No Records Available")

else:
    for i,r in enumerate(filtered_records,start=1):
        marks=r["marks"]
        if marks >= 90:
            grade="A"
        elif marks >=75 and marks<=89:
            grade="B"
        elif marks >= 60 and marks <=74:
            grade="C"
        else:
            grade="Fail"

        st.write("Record:", i)
        st.write("Time",r["time"])
        st.write("Name:", r["name"])
        st.write("Roll_no",r["roll_no"])
        st.write("Subjects",r["subjects"])
        st.write("Marks:", r["marks"])
        st.write("Grade:", grade)


# Performance Analytics
st.subheader("Performance Analytics")
if not st.session_state.student:
    st.info("No data available for analytics")
else:
    total_records=len(st.session_state.student)
    total_marks = 0
    highest_marks=st.session_state.student[0]["marks"]
    lowest_marks=st.session_state.student[0]["marks"]

    for r in st.session_state.student:
        marks=r["marks"]
        total_marks += marks
        if marks > highest_marks:
            highest_marks=marks
        if marks < lowest_marks:
            lowest_marks=marks
    average=total_marks/total_records

    st.write("Total Records:", total_records)
    st.write("Average Marks:", average)
    st.write("Highest Marks:", highest_marks)
    st.write("Lowest Marks:", lowest_marks)

# Subject-wise Average
st.subheader("Subject-wise Average")
if not st.session_state.student:
    st.info("No records available for subject-wise average")
else:

 subject_totals = {
    "Math": 0,
    "Science": 0,
    "English": 0,
    "Computer": 0
}

 subject_counts = {
    "Math": 0,
    "Science": 0,
    "English": 0,
    "Computer": 0
}
 for r in st.session_state.student:
    subjects=r["subjects"]
    marks=r["marks"]
    subject_totals[subjects] +=marks
    subject_counts[subjects] +=1
 for subject in subject_totals:
  if subject_counts[subject] > 0:
    average=subject_totals[subject]/subject_counts[subject]
    st.write(subject,":",average)
  else:
    st.write(subject,":","No records")

# Top performer
st.subheader("Top Performer ")
if not st.session_state.student:
    st.info("No records to determine top performer")
else:
    top_record=st.session_state.student[0]
    for r in st.session_state.student:
      if r["marks"] > top_record["marks"]:
        top_record=r
    st.success("🏆 Top Performer 🎉")
    st.write("Time", top_record["time"])
    st.write("Name:", top_record["name"])
    st.write("Roll_no", top_record["roll_no"])
    st.write("Subjects", top_record["subjects"])
    st.write("Marks:", top_record["marks"])

# delete and rest
col3,col4=st.columns(2)
with col3:
  if st.button("Delete Last Record"):
        if st.session_state.student:
            last =st.session_state.student.pop()
            st.session_state.last_action="Delete last record"
            st.success("Successfully deleted the last record")
        else:
            st.warning("No record to delete")

with col4:
  if st.button("Reset all"):
      st.session_state.student = []
      st.session_state.last_action = "Record reset"
      st.success("All records have been reset successfully")
      st.rerun()

st.info(f"Last Action: {st.session_state.last_action}")
