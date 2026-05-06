import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

df=pd.read_csv("pet_type.csv")
print(df)

# data preprocessing
# label encoding


le=LabelEncoder()
df["Furry"] = le.fit_transform(df["Furry"])
df["Barks"] = le.fit_transform(df["Barks"])
df["Size"] = le.fit_transform(df["Size"])
df["Pet"]= le.fit_transform(df["Pet"])
print(df)

# define x and y
x=df[["Furry","Barks","Size"]]
y=df["Pet"]

# train test splitting
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)

# model initiliaze
model = RandomForestClassifier(n_estimators=300,random_state=42)

# fit data into model
model.fit(x_train,y_train)

# prediction
prediction= model.predict(x_test)
print(le.inverse_transform(prediction))

accuracy=accuracy_score(y_test,prediction)
print(accuracy)