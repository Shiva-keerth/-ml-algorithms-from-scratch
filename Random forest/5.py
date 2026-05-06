import matplotlib.pyplot as plt
import streamlit as st

st.title("User-defined Chart")

selected = st.selectbox(
    "Types Of Graphs",
    ["bar", "barh", "pie", "scatter", "bubble", "histogram", "line", "multiline"]
)


# BAR
if selected == "bar":
    label_input = st.text_input("Enter Labels (X):", placeholder="a,b,c,d")
    values_input = st.text_input("Enter Values (Y):", placeholder="10,20,30,40")
    if st.button("Generate Bar Chart"):
        labels = label_input.split(",")
        values = [int(v) for v in values_input.split(",")]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_title("Bar Chart")
        st.pyplot(fig)

# BARH
if selected == "barh":
    label_input = st.text_input("Enter Labels (X):", placeholder="a,b,c,d")
    values_input = st.text_input("Enter Values (Y):", placeholder="10,20,30,40")
    if st.button("Generate Barh Chart"):
        labels = label_input.split(",")
        values = [int(v) for v in values_input.split(",")]

        fig, ax = plt.subplots()
        ax.barh(labels, values)
        ax.set_title("Barh Chart")
        st.pyplot(fig)

# PIE
if selected == "pie":
    label_input = st.text_input("Enter Labels (X):", placeholder="a,b,c,d")
    values_input = st.text_input("Enter Values (Y):", placeholder="10,20,30,40")
    if st.button("Generate Pie Chart"):
        labels = label_input.split(",")
        values = [int(v) for v in values_input.split(",")]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title("Pie Chart")
        st.pyplot(fig)

# SCATTER
if selected == "scatter":
    x_input = st.text_input("Enter X Values (for scatter):", placeholder="1,2,3,4")
    values_input = st.text_input("Enter Values (Y):", placeholder="10,20,30,40")
    if st.button("Generate Scatter Chart"):
        x = [int(i) for i in x_input.split(",")]
        values = [int(v) for v in values_input.split(",")]

        fig, ax = plt.subplots()
        ax.scatter(x,values)
        ax.set_title("Scatter Chart")
        st.pyplot(fig)

# BUBBLE
if selected == "bubble":
    # extra inputs for bubble
    bubble_x = st.text_input("Enter X values (for bubble):", placeholder="1,2,3,4")
    bubble_y = st.text_input("Enter Y values (for bubble):", placeholder="10,20,30,40")
    bubble_size = st.text_input("Enter Bubble Sizes:", placeholder="100,300,600,900")
    if st.button("Generate Bubble Chart"):
        x = [int(i) for i in bubble_x.split(",")]
        y = [int(i) for i in bubble_y.split(",")]
        sizes = [int(i) for i in bubble_size.split(",")]

        fig, ax = plt.subplots()
        ax.scatter(x, y, s=sizes, alpha=0.6)
        ax.set_title("Bubble Chart")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        st.pyplot(fig)


# HISTOGRAM
if selected == "histogram":
    values_input = st.text_input("Enter Values (Y):", placeholder="10,20,30,40")
    if st.button("Generate Histogram"):
        values = [int(v) for v in values_input.split(",")]

        fig, ax = plt.subplots()
        ax.hist(values)
        ax.set_title("Histogram")
        st.pyplot(fig)

# LINE
if selected == "line":
    label_input = st.text_input("Enter Labels (X):", placeholder="a,b,c,d")
    values_input = st.text_input("Enter Values (Y):", placeholder="10,20,30,40")
    if st.button("Generate Line Chart"):
        labels = label_input.split(",")
        values = [int(v) for v in values_input.split(",")]

        fig, ax = plt.subplots()
        ax.plot(labels, values)
        ax.set_title("Line Chart")
        st.pyplot(fig)

# MULTILINE
if selected == "multiline":
    label_input = st.text_input("Enter Labels (X):", placeholder="a,b,c,d")
    values_input = st.text_input("Enter Values (Y):", placeholder="10,20,30,40")
    # extra inputs for multiline
    multi_y1 = st.text_input("Enter Line 1 Y values (for multiline):", placeholder="10,20,30,40")
    multi_y2 = st.text_input("Enter Line 2 Y values (for multiline):", placeholder="5,15,25,35")
    multi_names = st.text_input("Enter Line Names (for multiline):", placeholder="Line1,Line2")
    if st.button("Generate Multiline Chart"):
        x_labels = label_input.split(",")

        y1 = [int(v) for v in multi_y1.split(",")]
        y2 = [int(v) for v in multi_y2.split(",")]

        line_names = multi_names.split(",")

        name1 = line_names[0] if len(line_names) > 0 else "Line 1"
        name2 = line_names[1] if len(line_names) > 1 else "Line 2"

        fig, ax = plt.subplots()
        ax.plot(x_labels, y1, label=name1)
        ax.plot(x_labels, y2, label=name2)
        ax.set_title("Multiline Chart")
        ax.legend()
        st.pyplot(fig)
