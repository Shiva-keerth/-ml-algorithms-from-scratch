import streamlit as st

st.title("Dynamic City Map")

city = st.chat_input("Type any city name")

if city:
    st.write(f"Showing Location for {city}")
    # Fixed iframe URL and component name
    st.components.v1.iframe(f"https://maps.google.com/maps?q={city}&t=&z=12&ie=UTF8&iwloc=&output=embed", height=500)