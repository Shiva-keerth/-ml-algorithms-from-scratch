import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

df=pd.read_csv("pet_type.csv")
print(df)

# data preprocessing
# label encoding
# print(df["Pet"])

le=LabelEncoder()
df["Furry"] = le.fit_transform(df["Furry"])
df["Barks"] = le.fit_transform(df["Barks"])
df["Size"] = le.fit_transform(df["Size"])
df["Pet"]= le.fit_transform(df["Pet"])
print(df)

# define x and y
x=df[["Furry","Barks","Size"]]
y=df[["Pet"]]

#  model selection
model= DecisionTreeClassifier()

# fit data into model
model.fit(x,y)

# prediction

new_data1 = [[1,1,1]]
predicition=model.predict(new_data1)
# print(prediciton)

transformed_predicition1=le.inverse_transform(predicition)
print(transformed_predicition1)