import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("mall_customers.csv")

#  Select features (ignore CustomerID)
X = df[["Annual_Income", "Spending_Score"]]

#  Apply scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#  Apply KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
y_kmeans = kmeans.fit_predict(X_scaled)

#  Add cluster labels to dataset
df["Cluster"] = y_kmeans

#  Plot clusters
plt.scatter(X_scaled[:,0], X_scaled[:,1], c=y_kmeans, cmap='viridis')
plt.xlabel("Annual Income (Scaled)")
plt.ylabel("Spending Score (Scaled)")
plt.title("K-Means Clustering")
plt.show()
