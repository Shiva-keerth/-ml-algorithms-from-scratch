import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# file read
df=pd.read_csv("improved_moviedataset.csv")

# data prprocessing
le=LabelEncoder()
df["genre"] = le.fit_transform(df["genre"])
print(df)

# define x and y
x=df.drop("genre",axis=1)
y=df["genre"]
print(x)
print(y)

# train and test
xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.4,random_state=42)

# scaling data
scaler =StandardScaler()
x_train_scaled=scaler.fit_transform(xtrain)
x_test_scaled =scaler.transform(xtest)

# initiliaze model
model=KNeighborsClassifier(n_neighbors=4)

# fir data into model
model.fit(x_train_scaled,ytrain)

# prediction
prediction =model.predict(x_test_scaled)

print(le.inverse_transform(prediction))

accuracy =accuracy_score(ytest,prediction)
print(accuracy)