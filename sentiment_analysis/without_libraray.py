import streamlit as st
positive_words = ["good","great","awsome","healthy","nice", "happy", "Love", "best"]
negative_words = ["sad", "bad", "hate","angry"]

text = st.text_input("Enter Sentence:").lower()

pos_count = 0
neg_count = 0

for word in text.split():
    if word in positive_words:
        pos_count += 1
    elif word in negative_words:
        neg_count += 1

if pos_count > neg_count:
    st.write("Sentiment positive")
elif neg_count > pos_count:
    st.write("Sentiment negative")
else:
    st.write("Sentiment neutral")