import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

df=pd.read_csv("master_decision.csv")

# data preprocessing
# label encoding

print(df["Placed"])

le=LabelEncoder()
df["Placed"] =le.fit_transform(df["Placed"])
df["GATE_Score"] =le.fit_transform(df["GATE_Score"])
df["Should_Do_Masters"] =le.fit_transform(df["Should_Do_Masters"])

print(df)

# define x and y
x=df[["Placed","GATE_Score","Salary"]]
y=df[["Should_Do_Masters"]]

#  model selection
model= DecisionTreeClassifier()

# fit data into model
model.fit(x,y)

# prediction
# Placed -- No(0),Yes(1)
# Gate Score -- AVG(0),GOOD(1),POOR(2)

new_data = [[0,50000,2]]
predicition=model.predict(new_data)
# print(prediciton)

transformed_predicition=le.inverse_transform(predicition)
print(transformed_predicition)