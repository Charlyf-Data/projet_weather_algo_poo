import streamlit as st
from ui.background import BackgroundManager


BackgroundManager(r"png\wallpaper\toulouse-france-skyline-2.jpg").apply()

st.header("Welcome to Weather subway Toulouse")

