import streamlit as st
from expolor_data import show_page, load_data

page = st.sidebar.selectbox("Exp or pred",("predict","Explore"))

if page == "predict":
    show_page()
else:
    load_data()

