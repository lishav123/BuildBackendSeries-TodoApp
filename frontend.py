import streamlit as st

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.success("Logged in")