import numpy as np
import pandas as pd
import streamlit as st
import pickle as pickle
import sklearn as sklearn

from sklearn.tree import DecisionTreeRegressor

def load_data():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
        return data


data = load_model()


def show_predictpage():
    st.title("Software Developer Salary Predictor")

    st.write("""### Provide the following information to predict the salary""")

    cou = st.selectbox("Country",countries)
    edu = st.selectbox("Education", education)
    exp = st.slider("Experience",min_value = 0,max_value = 50,value=3)

    ok = st.button("Calculate Salary")

    if ok is True:
        x = np.array([[cou,edu,exp]])
        x[:,0] = le_country_loaded.transform(x[:,0] )
        x[:, 1] = le_education_loaded.transform(x[:, 1])
        x = x.astype(float)
        out = regressor_loaded.predict(x)
        print(out)

        st.subheader(f"Estimated Salary is $ {out[0]:0.0f}")





