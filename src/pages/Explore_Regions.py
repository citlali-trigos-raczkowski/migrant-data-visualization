
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
df_w_cause = df.groupby(['Migration route','Cause of Death','date'])[['Total Number of Dead and Missing', 'Minimum Estimated Number of Missing',
                                                                          'Number of Females', 'Number of Males', 'Number of Children', 'Number of Survivors']].sum().reset_index()

df_wout_cause = df.groupby(['Migration route','date'])[['Total Number of Dead and Missing', 'Minimum Estimated Number of Missing',
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


def plot_deaths_month(m_route,cause, df_wout_cause,df_wcause):
    if len(cause) > 0:
        dft = df_wcause[(df_wcause['Migration route'] == m_route) & (df_wcause['Cause of Death'].isin(
        cause))].groupby(['Migration route','date'])[['Total Number of Dead and Missing', 'Minimum Estimated Number of Missing',
                                                                          'Number of Females', 'Number of Males', 'Number of Children']].sum().reset_index()
    else: 
        dft = df_wout_cause[df_wout_cause['Migration route'] == m_route]
    fig = px.line(dft, x='date', y=['Total Number of Dead and Missing','Number of Females', 'Number of Males', 'Number of Children'], title=f"Plot of deaths by month along the {m_route} route.")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.write(fig)

def plot_deaths_and_survivors_month(m_route,cause, df_wout_cause,df_wcause):
    if len(cause) > 0:
        dft = df_wcause[(df_wcause['Migration route'] == m_route) & (df_wcause['Cause of Death'].isin(
        cause))].groupby(['Migration route','date'])[['Total Number of Dead and Missing', 'Number of Survivors']].sum().reset_index()
    else: 
        dft = df_wout_cause[df_wout_cause['Migration route'] == m_route]
    fig = px.line(dft, x='date', y=['Total Number of Dead and Missing','Number of Survivors'], title=f"Plot of deaths and survivors by month along the {m_route} route." )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
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

cause_of_death_input = st.sidebar.multiselect(
    'Cause of Death', df['Cause of Death'].unique().tolist())
if len(cause_of_death_input) > 0:
    migrantdf = df[df['Cause of Death'].isin(
        cause_of_death_input)]


if route_input:
    route_s= route_input[0]
    plot_deaths_month(route_s,cause_of_death_input,df_wout_cause,df_w_cause)
    plot_deaths_and_survivors_month(route_s,cause_of_death_input,df_wout_cause,df_w_cause)
    plot_deaths_season(route_s, df1)
    plot_deaths_cause(route_s,cause_of_death_input, df2)

if len(route_input) > 0 and len(cause_of_death_input) > 0:
    plot_comp(route_input, cause_of_death_input, df2)



if route_input:

    mdf = df[df['Migration route'] == route_s]
    migrantdf = mdf.groupby(['Migration route'])[
    'Cause of Death'].agg(pd.Series.mode).reset_index()
    st.metric(f'Most common cause of death',migrantdf['Cause of Death'].iloc[0])
    col1,col2= st.columns(2)
    route_s= route_input[0]
    worst_month = mdf.groupby(['Migration route','date'])['Total Number of Dead and Missing'].sum().reset_index().sort_values(by='Total Number of Dead and Missing',ascending=False)
    df_d_s = mdf.groupby(['Migration route'])[['Total Number of Dead and Missing','Number of Survivors']].sum().reset_index()
    
    with col1:
        st.metric(f'Total number of Dead and Missing',df_d_s['Total Number of Dead and Missing'].iloc[0])
    with col2:
        st.metric(f'Number of Survivors',df_d_s['Number of Survivors'].iloc[0])
    col3,col4 = st.columns(2)
    with col3:
        st.metric(f'Deadliest event date',worst_month['date'].dt.strftime('%Y-%m').iloc[0])
    with col4:
        st.metric(f'Deadliest event number of deaths',worst_month['Total Number of Dead and Missing'].iloc[0])