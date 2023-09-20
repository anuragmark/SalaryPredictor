import streamlit as st
from predict import show_predictpage
from explore import show_exploredata

opt = st.sidebar.selectbox("Options",['Explore','Predict'])

if opt == 'Predict':
    show_predictpage()
else:
    show_exploredata()