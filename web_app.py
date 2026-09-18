import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="بوابة shawahed الرقمية", page_icon="🎓", layout="centered")

st.markdown("""
<style>
.stTextInput align-items { direction: rtl !important; text-align: right !important; }
.st_label { text-align: right !important; direction: rtl !important; width: 100%; }
.stButton button { direction: rtl !important; }
div[data-baseweb="input"] { 
    direction: rtl !important; 
    text-align: right !important; 
    border: 2px solid #1E3A8A !important;
    border-radius: 8px !important;
    background-color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)
