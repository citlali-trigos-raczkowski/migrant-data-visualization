import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def get_data():
    return pd.read_csv("../data/data.csv")

tweet_df = get_data()

def plot_deaths_month(route, df):
    route_df = df[df['route'] == route]
    fig = px.bar(route_df, x='date', y=['number dead','number missing'], title=f"Plot of deaths/missing by month along the {route} route.")
    fig.update_xaxes(range=['2022-08-01','2022-11-01'])
    fig.update_traces(width=100000000)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis_title':"Date", 
        'yaxis_title':"Number of Deaths/Missing"
    })
    st.write(fig)

def tweet_embed(tweet_url):
    link = f'https://publish.twitter.com/oembed?url={tweet_url}'
    resp = requests.get(link)
    rjs = resp.json()['html']
    return rjs

# data after August
tweet_df = tweet_df.loc[(tweet_df['date'] >= '2022-08-01')]
tweet_df['date'] = pd.to_datetime(tweet_df['date'])

tweet_df['number dead'] = tweet_df['number dead'].astype(int)
tweet_df['number missing'] = tweet_df['number missing'].astype(int)

df1 = tweet_df.groupby(['route','date'])[['number dead', 'number missing']].sum().reset_index()

# Page: Twitter Integration
st.header("Twitter API Integration for More Recent Data")

st.markdown('We used the Twitter API to download tweets from specific accounts that often report on news relating to migrants and search-and-rescue \
operations, as well as Tweets matching a search with the keywords "migrant missing dead". Downloading Tweets from specified users \
necessitated an Elevated Access to the API, and our request for this was approved. The "search" function of the API was able to give \
results for the last 7 days. A thousand Tweets per user were downloaded from the users [@USCGSoutheast](https://twitter.com/USCGSoutheast), \
[@SARwatchMED](https://twitter.com/SARwatchMED) and [@InfoMigrants](https://twitter.com/infomigrants?lang=en), all of which report on \
incidents relating to migrants, and the keyword search for Tweets from the last 7 days resulted in 61 Tweets.')

st.markdown('Below is an example of a Tweet from InfoMigrants.')

t_link = 'https://twitter.com/InfoMigrants/status/1579465035780304896'
example_tweet = tweet_embed(t_link)

components.html(example_tweet, height=500)

st.markdown('After downloading the Tweets, we filtered the ones relating to incidents by choosing ones containing keywords such as migrant, missing, \
etc. From reading these and writing down data, we were able to obtain a dataset of recent incidents containing the number of people dead/missing, \
location/migratory route, and the date when it was reported for each incident.')

st.markdown('Below is an example of what the dataset looks like.')
st.dataframe(df1.head(7))

st.markdown('Nearly all of the data was from the Mediterranean. This is likely due to fact that according to data from the Missing Migrants Project, \
Mediterranean routes are the ones with the most incidents, and can also partly be because one the sources was [@SARwatchMED](https://twitter.com/SARwatchMED), \
which exclusively reports on search-and-rescue operations on the Mediterranean.')

st.markdown('From the Data Filters in the left menu, you can choose the route you want to see the data for. The graph below shows the number of deaths and missing. ')

st.sidebar.write("Data Filters")
route_input = [st.sidebar.selectbox(
    'Migration Route', tweet_df['route'].unique().tolist())]

if route_input:
    route_s = route_input[0]
    plot_deaths_month(route_s, df1)
