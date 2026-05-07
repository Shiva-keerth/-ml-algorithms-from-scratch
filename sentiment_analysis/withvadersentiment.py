import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
text = st.text_input("Enter Sentence")
score = analyzer.polarity_scores(text)
st.write("Scores", score)

if score["compound"] >= 0.5:
    st.write("Sentiment Positive")
elif score["compound"] <= 0.5:
    st.write("Sentiment Negative")
else:
    st.write("Sentiment neutral")