import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache_data
def load_data():
    df = pd.read_csv('https://drive.google.com/uc?id=13FGuiABQkTNbBDKJ_4JUGGUmy3KlJKpG')
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()



def show_explore_page():
    st.title("Informasi berdasarkan Data Survey Public")

    #st.write(
    ''''''
    #)

    st.write(""" # Jumlah Data dari berbagai Country""")

    data = df["Country"].value_counts()
    dataCountry = df["Country"]

    colors= ['#03045e4', '#262d79', '#475492', '#677bab', '#88a2c4', '#a9c9dd', '#caf0f6']
    
    # Membuat pie chart menggunakan Plotly
    fig = go.Figure(data=[go.Pie(labels=dataCountry, values=data, marker=dict(colors=colors))])
    fig.update_traces(textposition='inside', textinfo='label+percent')

    
    # Menampilkan pie chart menggunakan Streamlit
    st.plotly_chart(fig)
    #fig1, ax1 = plt.subplots(figsize=(11, 12))
    #ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    #ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    #st.pyplot(fig1)
    
    st.write(
        """
    # Rata-rata Gaji berdasarkan Negara
    """
    )

    #data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    #st.bar_chart(data)

    # Menghitung rata-rata gaji berdasarkan negara dan mengurutkannya
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=False)

# Membuat bar chart menggunakan Plotly
    fig = go.Figure(data=go.Bar(
    x=data.index,  # Negara sebagai sumbu x
    y=data.values,  # Rata-rata gaji sebagai sumbu y
    marker=dict(color=data.values, colorscale='viridis'),  # Skema warna Inferno
))

# Menampilkan bar chart menggunakan Streamlit
    st.plotly_chart(fig)

    st.write(
        """
    # Rata-rata Gaji berdasarkan Pengalaman Kerja
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)