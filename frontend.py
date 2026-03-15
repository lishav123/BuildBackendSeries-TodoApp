import streamlit as st

if "login" not in st.session_state:
    st.session_state.login = True
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("Login" if st.session_state.login else "Register")

    if not st.session_state.login:
        username = st.text_input("Username")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login" if st.session_state.login else "Register"):
        st.success("Logged in" if st.session_state.login else "Registered")
        st.session_state.authenticated = True
        st.rerun()

    if st.button("Don't have account? Register" if st.session_state.login else "Already have an account? Login"):
        st.session_state.login = not st.session_state.login
        st.rerun()

else:
    task = st.text_input("Enter your task")
    button = st.button("Add the task")


    with st.sidebar:
        logout = st.button("Logout")

    if logout:
        st.session_state.authenticated = False
        st.rerun()