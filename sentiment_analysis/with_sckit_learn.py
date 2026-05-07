from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import streamlit as st


# training data
text = ["I love this product",
"This is amazing","I hate people",
"Worst Experience ever","Very good service",
"this could be better than that",
"very bad quality", "happy"]

labels = ["Positive", "Positive",
"Negative", "Negative", "Positive","Negative","Negative",
"Positive"]

# Convert text to numbers
vectorizer = CountVectorizer()
x = vectorizer.fit_transform(text)

# train model
model = MultinomialNB()
model.fit(x, labels)

# user input
user_input = st.text_input("Enter Sentence")
st.write(user_input)

input_vec = vectorizer.transform([user_input])


# predict
prediction = model.predict(input_vec)

st.write("Sentiment:",prediction[0])