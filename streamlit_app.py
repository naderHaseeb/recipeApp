import streamlit as st

st.title("My First Streamlit App")
st.write("Hello, this is my project app!")

name = st.text_input("Enter your name:")

if name:
    st.success(f"Welcome, {name}!")

