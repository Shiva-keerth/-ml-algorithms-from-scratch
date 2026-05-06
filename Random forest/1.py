import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# file read
df=pd.read_csv("master_decision.csv")

# data preprocess

le=LabelEncoder()
df["GATE_Score"]= le.fit_transform(df["GATE_Score"])
df["Should_Do_Masters"] = le.fit_transform(df["Should_Do_Masters"])

print(df)

# define x and y

x=df[["GATE_Score","Salary"]]
y=df["Should_Do_Masters"]

# train and test splitting

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=42)

# model initialize
model = RandomForestClassifier(n_estimators=150,random_state=42)

# fit data into model
model.fit(x_train,y_train)

# prediction
prediction= model.predict(x_test)
print(le.inverse_transform(prediction))

accuracy=accuracy_score(y_test,prediction)
print(accuracy)

newdata = [1,50000]
newprediction=model.predict(newdata)
print(le.inverse_transform(newprediction))