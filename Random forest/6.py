import streamlit as st
import matplotlib.pyplot as plt

st.title("Graph System")

graph = st.selectbox(
    "Select Graph Type",
    ["Bar", "Line", "Area", "Scatter", "Step", "Stem",
     "Multi Line", "Bubble", "Pie", "Histogram", "Box", "Violin"]
)

st.subheader("Enter Graph Details")

title = st.text_input("Enter Graph Title")
x_label = st.text_input("Enter X Label")
y_label = st.text_input("Enter Y Label")


# -------- Helper Functions -------- #

def num_list(text):
    text = text.replace(",", " ")
    return [float(i) for i in text.split()]


def str_list(text):
    text = text.replace(",", " ")
    return [i for i in text.split()]


# -------- Input Fields Based on Graph -------- #

if graph in ["Bar", "Line", "Area", "Scatter", "Step", "Stem"]:
    x_input = st.text_input("Enter X values")
    y_input = st.text_input("Enter Y values")

elif graph == "Multi Line":
    x_input = st.text_input("Enter X values")
    y1_input = st.text_input("Enter Y1 values")
    y2_input = st.text_input("Enter Y2 values")
    line1_label = st.text_input("Enter Line 1 Label")
    line2_label = st.text_input("Enter Line 2 Label")

elif graph == "Bubble":
    x_input = st.text_input("Enter X values")
    y_input = st.text_input("Enter Y values")
    size_input = st.text_input("Enter Bubble Sizes")

elif graph == "Pie":
    labels_input = st.text_input("Enter Labels")
    values_input = st.text_input("Enter Values")

elif graph in ["Histogram", "Box", "Violin"]:
    data_input = st.text_input("Enter Data values")

    if graph == "Histogram":
        bins = st.number_input("Enter number of bins", min_value=1, value=5)


# -------- Plot Button -------- #

if st.button("Generate Graph"):
    fig, ax = plt.subplots()

    try:

        if graph == "Bar":
            x = str_list(x_input)
            y = num_list(y_input)

            if len(x) != len(y):
                st.error("X and Y must have same length")
            else:
                ax.bar(x, y)

        elif graph == "Line":
            x = num_list(x_input)
            y = num_list(y_input)

            if len(x) != len(y):
                st.error("X and Y must have same length")
            else:
                ax.plot(x, y)

        elif graph == "Area":
            x = num_list(x_input)
            y = num_list(y_input)
            ax.fill_between(x, y)

        elif graph == "Scatter":
            x = num_list(x_input)
            y = num_list(y_input)
            ax.scatter(x, y)

        elif graph == "Step":
            x = num_list(x_input)
            y = num_list(y_input)
            ax.step(x, y)

        elif graph == "Stem":
            x = num_list(x_input)
            y = num_list(y_input)
            ax.stem(x, y)

        elif graph == "Multi Line":
            x = num_list(x_input)
            y1 = num_list(y1_input)
            y2 = num_list(y2_input)

            if not (len(x) == len(y1) == len(y2)):
                st.error("All inputs must have same length")
            else:
                ax.plot(x, y1, label=line1_label)
                ax.plot(x, y2, label=line2_label)
                ax.legend()

        elif graph == "Bubble":
            x = num_list(x_input)
            y = num_list(y_input)
            size = num_list(size_input)

            if not (len(x) == len(y) == len(size)):
                st.error("All inputs must have same length")
            else:
                ax.scatter(x, y, s=size)

        elif graph == "Pie":
            labels = str_list(labels_input)
            values = num_list(values_input)

            if len(labels) != len(values):
                st.error("Labels and Values must have same length")
            else:
                ax.pie(values, labels=labels, autopct="%1.1f%%")

        elif graph == "Histogram":
            data = num_list(data_input)
            ax.hist(data, bins=bins)

        elif graph == "Box":
            data = num_list(data_input)
            ax.boxplot(data)

        elif graph == "Violin":
            data = num_list(data_input)
            ax.violinplot(data)

        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(True)

        st.pyplot(fig)

    except:
        st.error("Invalid input format")
