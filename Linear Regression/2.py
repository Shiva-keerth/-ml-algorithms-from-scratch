import pandas as pd
from sklearn import linear_model

# load csv file

df = pd.read_csv("Book2.csv")
print(df)

print(df[["users"]])
print(df[["orders"]])

# define x and y

x= df[["users","orders"]]
y = df[["amount"]]

# model selection

reg = linear_model.LinearRegression()

# fit data into model

reg.fit(x,y)

# prediction

prediction = reg.predict([[4000,10000]])

print(prediction)

print(reg.coef_)
print(reg.intercept_)