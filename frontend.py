import streamlit as st
import requests


if "name" not in st.session_state:
    st.session_state.name = None

if "login" not in st.session_state:
    st.session_state.login = True

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("Login" if st.session_state.login else "Register")

    username = None
    if not st.session_state.login:
        username = st.text_input("Username")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login" if st.session_state.login else "Register"):
        if not st.session_state.login:
            status_code = requests.post("http://127.0.0.1:8000/register",
                          json={"username": username, "email": email, "password": password})
            if status_code.status_code == 400:
                st.info(status_code.json()["detail"])
            else:
                st.success("Logged in" if st.session_state.login else "Registered")
                st.session_state.authenticated = True
                st.session_state.name = username
                st.rerun()
        else:
            status_code = requests.post("http://127.0.0.1:8000/login",
                                        json={"email": email, "password": password})
            if status_code.status_code == 400:
                st.error(status_code.json()["detail"])
            else:
                st.success("Logged in" if st.session_state.login else "Registered")
                st.session_state.authenticated = True
                st.session_state.name = status_code.json()["username"]
                st.rerun()

    if st.button("Don't have account? Register" if st.session_state.login else "Already have an account? Login"):
        st.session_state.login = not st.session_state.login
        st.rerun()

else:
    st.title(f"Welcome, {st.session_state.name}!")
    task = st.text_input("Enter your task")
    button = st.button("Add the task")
    print(st.session_state.name)

    with st.sidebar:
        logout = st.button("Logout")

    if logout:
        st.session_state.authenticated = False
        st.rerun()