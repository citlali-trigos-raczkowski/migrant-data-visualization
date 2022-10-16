
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# TODO: get the data by uncommenting the below line (imports not working for me rn)
# from '../Home' import get_df
# instead reloading the data 😰


@st.cache
def get_data():
    return pd.read_csv("../Missing_Migrants_Global_Figures_filtered.csv")


df = get_data().rename(columns={"X": "lon", "Y": "lat"})

df['date'] = df[['Incident year','Reported Month']].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
df['date'] = df['date'] + '-1'
df['date'] = pd.to_datetime(df['date'])
migrantdf = df
# Prepare the data
df1 = df.groupby(['Migration route', 'Season', 'Incident year'])[
    'Total Number of Dead and Missing'].sum().reset_index(name='count')
df2 = df.groupby(['Migration route', 'Cause of Death', 'Cause of Death Abbreviation'])[
    'Total Number of Dead and Missing'].sum().reset_index(name='Total Number of Dead and Missing')
df3 = df.groupby(['Migration route', 'date'])[['Total Number of Dead and Missing', 'Minimum Estimated Number of Missing',
                                                                          'Number of Females', 'Number of Males', 'Number of Children', 'Number of Survivors']].sum().reset_index()

# Functions to create the graphs


def plot_deaths_season(m_route, df):
    '''Given a route, writes a line plot of deaths by season'''
    dft = df[df['Migration route'] == m_route]

    fig = px.line(dft, x='Incident year', y='count',
                  color='Season', title=f"Total deaths per Season in {m_route}")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.write(fig)


# Still in Development, i don't know how to show it
def plot_deaths_month(m_route, df):
    dft = df[df['Migration route'] == m_route]
    fig = px.line(dft, x='date', y='Total Number of Dead and Missing', title=f"Deaths per month in {m_route}")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.markdown("Plot of deaths by season along the " + m_route + "route.")
    st.write(fig)


def plot_deaths_cause(m_route, causes, df):
    dft = df[df['Migration route'] == m_route].sort_values(
        by='Total Number of Dead and Missing', ascending=False).reset_index()
    if causes:
        colors = ['lightslategray', ] * dft.shape[0]
        for i in causes:
            try:
                index = dft[dft['Cause of Death'] == i].index
                colors[index[0]] = 'crimson'
            except:
                pass
        fig = px.bar(dft, x='Cause of Death Abbreviation', y='Total Number of Dead and Missing',
                     title=f"Cause of Death in {m_route}", color=colors)
    else:
        fig = px.bar(dft, x='Cause of Death Abbreviation', y='Total Number of Dead and Missing',
                     title=f"Cause of Death in {m_route}")

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    st.write(fig)


def plot_comp(m_route, cause, df):
    dft = df[(df['Migration route'].isin(m_route)) & (df['Cause of Death'].isin(
        cause))].sort_values(by='Total Number of Dead and Missing', ascending=False)
    fig = px.bar(dft, x='Cause of Death Abbreviation', y='Total Number of Dead and Missing', color='Migration route', barmode='group',
                 title="Number of Dead by Cause of Death")

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    st.write(fig)


#  Markdown for the page
st.header("Explore One Region at a Time")
st.markdown("In this page we welcome you to explore the data one region at a time, using the filters in the left side menu to filter.")
st.sidebar.write("Data Filters")
route_input = [st.sidebar.selectbox(
    'Migration Route', df['Migration route'].unique().tolist())]
if len(route_input) > 0:
    migrantdf = df[df['Migration route'].isin(route_input)]
    show_route_death = True

cause_of_death_input = st.sidebar.multiselect(
    'Cause of Death', df['Cause of Death'].unique().tolist())
if len(cause_of_death_input) > 0:
    migrantdf = df[df['Cause of Death'].isin(
        cause_of_death_input)]


if len(route_input) > 0:
    for i in route_input:
        # st.map(migrantdf)
        plot_deaths_season(i, df1)
        plot_deaths_cause(i, cause_of_death_input, df2)
        plot_deaths_month(i,df3)

if len(route_input) > 0 and len(cause_of_death_input) > 0:
    plot_comp(route_input, cause_of_death_input, df2)
