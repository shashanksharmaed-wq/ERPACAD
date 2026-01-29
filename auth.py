import streamlit as st

USERS = {
    "t1": {"password": "t1pass", "role": "teacher"},
    "t2": {"password": "t2pass", "role": "teacher"},
    "principal": {"password": "admin123", "role": "principal"},
}

def login():
    if "user" in st.session_state:
        return True

    st.subheader("🔐 Login")

    user = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in USERS and USERS[user]["password"] == pwd:
            st.session_state.user = user
            st.session_state.role = USERS[user]["role"]
            st.rerun()
        else:
            st.error("Invalid credentials")

    return False

def logout():
    st.session_state.clear()
    st.rerun()
