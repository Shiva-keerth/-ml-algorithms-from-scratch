import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter =0

if "last_action" not in st.session_state:
    st.session_state.last_action ="None"

col1,col2 =st.columns(2)

with col1:
    if st.button("Increase"):
        st.session_state.counter +=1
        st.session_state.last_action ="Increase"

with col2:
    if st.button("Decrease"):
        st.session_state.counter -=1
        st.session_state.last_action ="Decrease"

st.subheader(f"Current count:{st.session_state.counter}")
st.write("Last action performed is",st.session_state.last_action)
st.write(st.session_state)