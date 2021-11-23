import streamlit as st

def app():
    st.title("History")
    st.sidebar.text_input("Please Enter Your Full Name:")
    st.sidebar.button("Submit")