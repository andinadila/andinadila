import streamlit as st
from streamlit.type_util import data_frame_to_bytes
import pandas as pd

def app():
    st.title("Upload File")
    
    uploaded_file = st.file_uploader("Choose a file", type=['csv','xlsx'])
    global data 
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            print(e)
            data = pd.read_excel(uploaded_file)