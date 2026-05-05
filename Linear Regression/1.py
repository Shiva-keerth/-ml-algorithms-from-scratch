import pandas as pd
from sklearn import linear_model

# load csv file

df = pd.read_csv("price.csv")
print(df)

print(df[["Area"]])

# define x and y

x = df[["Area"]]
y = df[["Price"]]

# model selection

reg = linear_model.LinearRegression()

# fit data into model

reg.fit(x,y)

# prediction

prediction = reg.predict([[2000]])

print(prediction)

print(reg.coef_)
print(reg.intercept_)