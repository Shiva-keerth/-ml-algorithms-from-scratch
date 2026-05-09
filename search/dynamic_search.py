import streamlit as st

st.title("Search Anything")

query = st.text_input("Search")

if query:
    search_url = f"https://www.google.com/search?q={query}"
    st.write("Click below to view result")
    st.link_button(label="Open search result", url=search_url)