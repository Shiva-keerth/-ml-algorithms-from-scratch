import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

df=pd.read_csv("transport_mode.csv")
print(df)

# data preprocessing
# label encoding
# print(df["ShirtSize"])

le=LabelEncoder()
df["Weather"] = le.fit_transform(df["Weather"])
df["Transport"]= le.fit_transform(df["Transport"])
print(df)

# define x and y
x=df[["Distance","Time","Weather"]]
y=df["Transport"]

# train and test splitting
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

# model intiliaze
model=RandomForestClassifier(n_estimators=250,random_state=42)

# fit data into model
model.fit(x_train,y_train)

# prediction
prediction= model.predict(x_test)
print(le.inverse_transform(prediction))

accuracy=accuracy_score(y_test,prediction)
print(accuracy)