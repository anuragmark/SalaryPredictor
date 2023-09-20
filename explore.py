import numpy as np
import pandas as pd
import streamlit as st
import pickle as pickle
import sklearn as sklearn
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeRegressor
countries = ['United States of America', 'United Kingdom', 'Australia',
       'Netherlands', 'Germany', 'Sweden', 'France', 'Spain', 'Brazil',
       'Italy', 'Canada', 'Switzerland', 'India', 'Norway', 'Denmark',
       'Israel', 'Poland']
countries.sort()

education = ['Less Than a Bachelors', "Master's Degree", 'Post Grad',"Bachelor's Degree"]

#@st.cache_data
def load_data():
    df = pd.read_csv("data/survey_results_public.csv")

    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)

    df = df[df['Salary'].notnull()]

    df = df.dropna()

    df = df[df['Employment'] == 'Employed, full-time']

    country_list = list(df.Country.value_counts()[df.Country.value_counts() <= 400].index)

    df.loc[df['Country'].isin(country_list), 'Country'] = 'Other'
    df.loc[df['Country'] == 'United Kingdom of Great Britain and Northern Ireland', 'Country'] = 'United Kingdom'

    df = df[df['Salary'] <= 300000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']

    def experience(x):
        if x == 'Less than 1 year':
            return 0.5
        elif x == 'More than 50 years':
            return 50
        return float(x)

    df['YearsCodePro'] = df['YearsCodePro'].apply(experience)

    def education(x):
        if x == 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)':
            return 'Bachelor\'s Degree'
        elif x == 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)':
            return 'Master\'s Degree'
        elif x == 'Professional degree (JD, MD, Ph.D, Ed.D, etc.)':
            return 'Post Grad'
        else:
            return 'Less Than a Bachelors'

    df['EdLevel'] = df['EdLevel'].apply(education)

    return df


df = load_data()
print(df.EdLevel.value_counts())

def show_exploredata():
    st.title("Explore Salary Trends")

    st.write("""### Based on the Stack Overflow Survey data for 2023""")
    st.write("")

    st.write("""##### 1. Salaries distribution across countries""")

    plt.figure(figsize=(30, 15))
    plot = sns.boxplot(x=df['Country'], y=df['Salary'])
    plt.xticks(rotation=90)
    plt.show()
    st.pyplot(plot.get_figure())

    st.write("")
    st.write("""##### 2. Salaries across different education levels""")
    country = st.selectbox("Country",countries)

    fig, axs = plt.subplots(1, 4, figsize=(20, 10), sharex=True, sharey=True)
    plt.tight_layout()
    sns.histplot(ax=axs[0], x=df[(df['Country'] == country) & (df['EdLevel'] == 'Bachelor\'s Degree')]['Salary'],
                      binwidth=10000)
    axs[0].set_title('Bachelors Degree')
    sns.histplot(ax=axs[1], x=df[(df['Country'] == country) & (df['EdLevel'] == 'Master\'s Degree')]['Salary'],
                 binwidth=10000)
    axs[1].set_title('Masters Degree')
    sns.histplot(ax=axs[2], x=df[(df['Country'] == country) & (df['EdLevel'] == 'Post Grad')]['Salary'], binwidth=10000)
    axs[2].set_title('Post Grad')
    sns.histplot(ax=axs[3], x=df[(df['Country'] == country) & (df['EdLevel'] == 'Less Than a Bachelors')]['Salary'],
                 binwidth=10000)
    axs[3].set_title('Less Than a Bachelors')

    st.pyplot(fig.get_figure())

    st.write("")
    st.write("""##### 3. Compare two countries""")

    c1,c2 = st.columns(2)
    with c1:
        country1 = st.selectbox("Country 1",countries)
    with c2:
        country2 = st.selectbox("Country 2", countries)
    degree = st.selectbox("Education",education)

    fig2,axs = plt.subplots(1,1,figsize=(20, 10))
    sns.lineplot(data=df[(df['Country'] == country1) & (df['EdLevel'] == degree)], x='YearsCodePro',
                 y='Salary', color='blue', estimator='mean', label=country1)
    sns.lineplot(data=df[(df['Country'] == country2) & (df['EdLevel'] == degree)], x='YearsCodePro',
                 y='Salary', color='green', estimator='mean', label=country2)
    st.pyplot(fig2.get_figure())

if __name__ == '__main__':
    show_exploredata()








