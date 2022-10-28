
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from millify import prettify

# TODO: get the data by uncommenting the below line (imports not working for me rn)
# from '../Home' import get_df
# instead reloading the data 😰


@st.cache
def get_data():
    return pd.read_csv("data/Missing_Migrants_Global_Figures_filtered.csv")


df = get_data().rename(columns={"X": "lon", "Y": "lat"})

df['date'] = df[['Incident year', 'Reported Month']].apply(
    lambda x: '-'.join(x.values.astype(str)), axis="columns")
df['date'] = df['date'] + '-1'
df['date'] = pd.to_datetime(df['date'])
migrantdf = df
# Prepare the data
df1 = df.groupby(['Migration route', 'Season', 'Incident year'])[
    'Total Number of Dead and Missing'].sum().reset_index(name='count')
df2 = df.groupby(['Migration route', 'Cause of Death', 'Cause of Death Abbreviation'])[
    'Total Number of Dead and Missing'].sum().reset_index(name='Total Number of Dead and Missing')
df_w_cause = df.groupby(['Migration route', 'Cause of Death', 'date'])[['Total Number of Dead and Missing', 'Minimum Estimated Number of Missing',
                                                                        'Number of Females', 'Number of Males', 'Number of Children', 'Number of Survivors']].sum().reset_index()

df_wout_cause = df.groupby(['Migration route', 'date'])[['Total Number of Dead and Missing', 'Minimum Estimated Number of Missing',
                                                        'Number of Females', 'Number of Males', 'Number of Children', 'Number of Survivors']].sum().reset_index()

# Functions to create the graphs


def plot_deaths_season(m_route, df):
    '''Given a route, writes a line plot of deaths by season'''
    dft = df[df['Migration route'] == m_route]

    fig = px.line(dft, x='Incident year', y='count',
                  color='Season', title=f"Total deaths per season in {m_route}")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis_title': "",
    })
    st.write(fig)


def plot_deaths_month(m_route, cause, df_wout_cause, df_wcause):
    if len(cause) > 0:
        dft = df_wcause[(df_wcause['Migration route'] == m_route) & (df_wcause['Cause of Death'].isin(
            cause))].groupby(['Migration route', 'date'])[['Total Number of Dead and Missing', 'Minimum Estimated Number of Missing',
                                                           'Number of Females', 'Number of Males', 'Number of Children']].sum().reset_index()
    else:
        dft = df_wout_cause[df_wout_cause['Migration route'] == m_route]
    fig = px.line(dft, x='date', y=['Total Number of Dead and Missing', 'Number of Females',
                  'Number of Males', 'Number of Children'], title=f"Plot of deaths by month along the {m_route} route.")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis_title': "",
        'yaxis_title': "Number of deaths",
    })
    st.write(fig)


def plot_deaths_and_survivors_month(m_route, cause, df_wout_cause, df_wcause):
    if len(cause) > 0:
        dft = df_wcause[(df_wcause['Migration route'] == m_route) & (df_wcause['Cause of Death'].isin(
            cause))].groupby(['Migration route', 'date'])[['Total Number of Dead and Missing', 'Number of Survivors']].sum().reset_index()
    else:
        dft = df_wout_cause[df_wout_cause['Migration route'] == m_route]
    fig = px.line(dft, x='date', y=['Total Number of Dead and Missing', 'Number of Survivors'],
                  title=f"Plot of deaths and survivors by month along the {m_route} route.")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis_title': "",
        'yaxis_title': "Number of deaths",
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
                     title=f"Causes of death in {m_route}", color=colors)
    else:
        fig = px.bar(dft, x='Cause of Death Abbreviation', y='Total Number of Dead and Missing',
                     title=f"Causes of death in {m_route}")

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis_title': "",
    })
    st.markdown(
        "Selecting a cause of death from the left side menu will modify the below plot(s).")
    st.write(fig)


def plot_comp(m_route, cause, df):
    dft = df[(df['Migration route'].isin(m_route)) & (df['Cause of Death'].isin(
        cause))].sort_values(by='Total Number of Dead and Missing', ascending=False)
    fig = px.bar(dft, x='Cause of Death Abbreviation', y='Total Number of Dead and Missing', color='Migration route', barmode='group',
                 title="Number of Deaths by cause of death")

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    st.write(fig)


#  Markdown for the page
st.header("Explore One Region at a Time")
st.markdown("In this page we welcome you to explore the data one region at a time, using the filters in the left side menu. Try selecting a new region to check how the data visualization changes. " +
            "Migrations often include families with children. While these journeys are dangerous, they are even moreso for children." + " For those that do survive the journey, it is often not without great difficulty and loss.")

st.markdown("The following is a table of all included migration routes paired with the total number of recorded dead and missing people from that route, since 2014.")
st.markdown("The data from the Missing Migrants Project includes instances in Asia that are not assigned any migration route. We have compiled these and assigned them the new value: `Routes in Asia`. In time we hope to understand these events in more detail.")
dff = df.groupby(['Migration route'])[
    ['Total Number of Dead and Missing']].sum().sort_values('Total Number of Dead and Missing', ascending=False).reset_index()
st.dataframe(dff)

st.sidebar.write("Data Filters")

route_input = [st.sidebar.selectbox(
    'Migration Route', df['Migration route'].unique().tolist())]
st.header('Exploring the '+route_input[0])


if route_input:
    route_s = route_input[0]
    mdf = df[df['Migration route'] == route_s]
    migrantdf = mdf.groupby(['Cause of Death'])[
        'Total Number of Dead and Missing'].sum().reset_index().sort_values(by='Total Number of Dead and Missing', ascending=False)
    route_s = route_input[0]
    worst_month = mdf.groupby(['Migration route', 'date'])['Total Number of Dead and Missing'].sum(
    ).reset_index().sort_values(by='Total Number of Dead and Missing', ascending=False)
    df_d_s = mdf.groupby(['Migration route'])[
        ['Total Number of Dead and Missing', 'Number of Survivors', 'Number of Females', 'Number of Males', 'Number of Children']].sum().reset_index()

    total_dead_missing = prettify(
        df_d_s['Total Number of Dead and Missing'].iloc[0])
    total_women_dead_missing = prettify(df_d_s['Number of Females'].iloc[0])
    total_men_dead_missing = prettify(df_d_s['Number of Males'].iloc[0])
    total_children_dead_missing = prettify(
        df_d_s['Number of Children'].iloc[0])

    # introduction
    st.markdown("For the " + route_input[0] +
                " migration route, there are a total of  " + total_dead_missing +
                " recorded deaths in the data since 2014. This includes " + total_women_dead_missing +
                " women, " + total_men_dead_missing + " men, and " + total_children_dead_missing + " children.")

    # Country of origin
    mdf['Number of People'] = mdf.loc[:, [
        'Total Number of Dead and Missing', 'Number of Survivors']].sum(axis=1)
    total_migrants = mdf['Number of People'].sum()
    mdf['Percentage of People from Country of Origin'] = mdf['Number of People']/total_migrants
    dforigin = mdf.groupby(['Country of Origin'])[['Number of People', 'Percentage of People from Country of Origin']].sum(
    ).sort_values('Number of People', ascending=False).reset_index()

    st.markdown("The following table lists the known countries of origin for migrants traveling along this route. For each country, we see the total number of people from the country and the percentage of migrants from the country.")
    st.dataframe(dforigin)

    #   column statistics
    st.subheader("View the Statistics")
    col1, col2 = st.columns(2)
    cause1 = migrantdf['Cause of Death'].iloc[0]
    st.metric(f'Most common cause of death', cause1)
    cause2 = migrantdf['Cause of Death'].iloc[1]
    st.metric(f'Second most common cause of death', cause2)

    with col1:
        st.metric(f'Total number of Recorded Dead and Missing since 2014',
                  total_dead_missing)
    with col2:
        st.metric(f'Number of Recorded Survivors',
                  prettify(df_d_s['Number of Survivors'].iloc[0]))
    col3, col4 = st.columns(2)
    with col3:
        st.metric(f'Deadliest event date',
                  worst_month['date'].dt.strftime('%Y-%m').iloc[0])
    with col4:
        st.metric(f'Deadliest event number of deaths',
                  prettify(worst_month['Total Number of Dead and Missing'].iloc[0]))


cause_of_death_input = st.sidebar.multiselect(
    'Cause of Death', df['Cause of Death'].unique().tolist())
if len(cause_of_death_input) > 0:
    migrantdf = df[df['Cause of Death'].isin(
        cause_of_death_input)]

st.markdown('\n\n\n')
st.subheader("Maps of Death by Year, Month, and Season")

st.markdown("Each of the following graphs can be expanded using the expanding arrows button that appears to the right of the graph on hover. The graphs are interactive and scalable.")

if route_input:

    plot_deaths_month(route_s, cause_of_death_input, df_wout_cause, df_w_cause)
    plot_deaths_and_survivors_month(
        route_s, cause_of_death_input, df_wout_cause, df_w_cause)
    plot_deaths_season(route_s, df1)
    plot_deaths_cause(route_s, cause_of_death_input, df2)

if len(route_input) > 0 and len(cause_of_death_input) > 0:
    plot_comp(route_input, cause_of_death_input, df2)
