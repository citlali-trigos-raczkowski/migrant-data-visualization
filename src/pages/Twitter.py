import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#from Home import get_df

def get_data():
    return pd.read_csv("../data/data.csv")

tweet_df = get_data()
#tweet_df = get_df

def plot_deaths_month(route, df):
    route_df = df[df['route'] == route]
    fig = px.bar(route_df, x='date', y=['number dead','number missing'], title=f"Plot of deaths/missing by month along the {route} route.")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis_title':"Date", 
        'yaxis_title':"Number of Deaths/Missing",
    })
    st.write(fig)

tweet_df['date'] = pd.to_datetime(tweet_df['date'])

# transform date column to months
#tweet_df['date'] = tweet_df['date'].dt.to_period('M').astype(str)

tweet_df['number dead'] = tweet_df['number dead'].astype(int)
tweet_df['number missing'] = tweet_df['number missing'].astype(int)

# data after August
tweet_df = tweet_df.loc[(tweet_df['date'] >= '2022-08-01')]

df1 = tweet_df.groupby(['route','date'])[['number dead', 'number missing']].sum().reset_index()

# Page: Twitter Integration
st.header("Twitter API Integration")

st.markdown('We used the Twitter API to download tweets, from specific accounts that often report on news relating to migrants and search \
and rescue operations, as well as tweets matching a search with the keywords "migrant missing dead". Downloading tweets for specified users \
necessitated the Elevated Access to the API, and our request was approved. The twitter "search" function of the API was able to give \
results for the last 7 days. A thousand tweets were downloaded from the users @USCGSoutheast, @SARwatchMED and @InfoMigrants, all of which report on incidents relating to migrants.')
st.markdown('Nearly all of the data was from the mediterranian, since according to data from the Missing Migrants Project, mediterranian routes are the ones with most incidents, and possibly due to the fact that one the sources was @SARwatchMED, which \
exclusively reports on the search-and-rescue operations on the Mediterranian.')
st.markdown('From the left menu, you can choose the route you want to see the data for. The graph below shows the number of deaths and missing. ')

st.sidebar.write("Data Filters")
route_input = [st.sidebar.selectbox(
    'Migration Route', tweet_df['route'].unique().tolist())]

if route_input:
    route_s= route_input[0]
    plot_deaths_month(route_s,df1)

