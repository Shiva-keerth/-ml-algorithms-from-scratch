import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        "KNNCLASSIFIER",
        ["Dataset", "Display"],
        icons=["table", "activity"],
        menu_icon="cast",
        default_index=0
    )
if selected == "Dataset":
 # Load dataset
 df = pd.read_csv("mall_customers.csv")
 st.write(df)

if selected == "Display":
 #  Select features (ignore CustomerID)
 df = pd.read_csv("mall_customers.csv")
 X = df[["Annual_Income", "Spending_Score"]]

#  Apply scaling
 scaler = StandardScaler()
 X_scaled = scaler.fit_transform(X)

 #  Apply KMeans
 kmeans = KMeans(n_clusters=3, random_state=42)
 y_kmeans = kmeans.fit_predict(X_scaled)

 #  Add cluster labels to dataset
 df["Cluster"] = y_kmeans

 # #  Plot clusters
 # plt.scatter(X_scaled[:,0], X_scaled[:,1], c=y_kmeans, cmap='viridis')
 # plt.xlabel("Annual Income (Scaled)")
 # plt.ylabel("Spending Score (Scaled)")
 # plt.title("K-Means Clustering")
 # plt.show()
 fig,ax1=plt.subplots()
 ax1.scatter(X_scaled[:,0], X_scaled[:,1], c=y_kmeans, cmap='viridis')
 ax1.set_xlabel("Annual Income (Scaled)")
 ax1.set_ylabel("Spending Score (Scaled)")
 ax1.legend()
 st.pyplot(fig)

