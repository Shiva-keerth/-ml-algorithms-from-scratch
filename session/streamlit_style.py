import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected=option_menu("Menu",["Home"],
                         icons=["house"],
                         styles={
                             "container":{"padding":"5px","background-color":"pink"},
                             "icon":{"font-size":"20px","color":"orange"},
                             "nav-link":{"font-size":"16px","text_align":"left"},
                             "nav-link-selected":{"background-color":"blue"}
                         },default_index=0)

if selected =="Home":
    if "Likes" not in st.session_state:
        st.session_state.Likes = 0

    if "Dislikes" not in st.session_state:
        st.session_state.Dislikes = 0

    # if "last_action" not in st.session_state:
    #     st.session_state.last_action = "None"

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Likes"):
            st.session_state.Likes += 1
            st.session_state.last_action = "Like"
    st.subheader(f"Current Likes:{st.session_state.Likes}")

    with col2:
        if st.button("Dislike"):
            st.session_state.Dislikes += 1
            st.session_state.last_action = "Dislike"
    st.subheader(f"Current Dislikes:{st.session_state.Dislikes}")

    if (st.session_state.Likes > st.session_state.Dislikes):
        st.write("Your reel has become viral")



    # st.write("Last action performed is", st.session_state.last_action)
    # st.write(st.session_state)

