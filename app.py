import streamlit as st
from predict import show_predictpage

opt = st.sidebar.selectbox("Options",['Explore','Predict'])

if opt == 'Predict':
    show_predictpage()
else:
    pass