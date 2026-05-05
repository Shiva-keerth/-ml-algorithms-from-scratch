import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

df=pd.read_csv("shirt_size.csv")
print(df)

# data preprocessing
# label encoding
print(df["ShirtSize"])

le=LabelEncoder()
df["ShirtSize"]= le.fit_transform(df["ShirtSize"])
print(df)

# define x and y
x=df[["Height","Weight"]]
y=df[["ShirtSize"]]

#  model selection
model= DecisionTreeClassifier()

# fit data into model
model.fit(x,y)

# prediction

new_data1 = [[190,70]]
predicition=model.predict(new_data1)
# print(prediciton)

transformed_predicition1=le.inverse_transform(predicition)
print(transformed_predicition1)