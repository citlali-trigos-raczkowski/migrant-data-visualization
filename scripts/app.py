import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Note 0: No longer using the Points (X,Y) because streamlit relies on
# longitude latitude, instead of (X,Y) coordinates
# See docs: https://docs.streamlit.io/library/api-reference/charts/st.map
#  
# from shapely.geometry import Point
# geometry = [Point(xy) for xy in zip(migrantdf.X, migrantdf.Y)]
# gdf = gpd.GeoDataFrame(migrantdf, crs="EPSG:4326", geometry=geometry)

# Note 1: Columns in our dataframe (migrantdf.columns):
# ['Unnamed: 0', 'Main ID', 'Incident ID', 'Incident Type',
#    'Region of Incident', 'Incident year', 'Reported Month',
#    'Number of Dead', 'Minimum Estimated Number of Missing',
#    'Total Number of Dead and Missing', 'Number of Survivors',
#    'Number of Females', 'Number of Males', 'Number of Children',
#    'Country of Origin', 'Region of Origin', 'Cause of Death',
#    'Migration route', 'Location of death', 'Information Source',
#    'Coordinates', 'UNSD Geographical Grouping', 'X', 'Y']

# Import the data
data_url = "../Missing_Migrants_Global_Figures_filtered.csv"
@st.cache
def get_data():
    url = data_url
    return pd.read_csv(url)
df = get_data()

st.title("Visualizing Deaths of Migrants at Borders")
st.markdown("Data collected by the Missing Migrant Project spanning years 2014 - 2022.")

# 0. Let's build the interactive map

# 1. Streamlit needs lat and lon columns to plot points
# TODO: THIS IS NOT CORRECT. Need a transformation for (X,Y) --> long,lat
df = df.rename(columns={"X": "lat", "Y": "lon"})

migrantdf = df

# 2. Add filter by migration route to sidebar
route_input = st.sidebar.multiselect('Migration Route', df['Migration route'].unique().tolist())
if len(route_input) > 0:
    migrantdf = df[df['Migration route'].isin(route_input)]

# 3. Add filter by cause of death to sidebar
cause_of_death_input = st.sidebar.multiselect('Cause of Death', df['Cause of Death'].unique().tolist())
if len(cause_of_death_input) > 0:
    migrantdf = df[df['Cause of Death'].isin(cause_of_death_input)]

st.map(migrantdf)

st.markdown("Data for the above visualization can be explored below:")

df1 = df.groupby(['Migration route','Season','Incident year'])['Total Number of Dead and Missing'].sum().reset_index(name='count')
df2 = df.groupby(['Migration route','Cause of Death'])['Total Number of Dead and Missing'].sum().reset_index(name='Total Number of Dead and Missing')

def plot_deaths_season(m_route,df):
    dft = df[df['Migration route'] == m_route]

    fig = px.line(dft,x='Incident year',y='count',color='Season',title=f"Deaths per Season in {m_route}")

    st.write(fig)

def plot_deaths_cause(m_route,df):
    dft = df[df['Migration route'] == m_route].sort_values(by='Total Number of Dead and Missing',ascending=False)
    fig = px.bar(dft,x='Cause of Death',y='Total Number of Dead and Missing',
            title=f"Cause of Death in {m_route}")

    st.write(fig)

def plot_comp(m_route,cause,df):
    dft = df[(df['Migration route'].isin( m_route)) & (df['Cause of Death'].isin(cause))].sort_values(by='Total Number of Dead and Missing',ascending=False)
    fig = px.bar(dft,x='Cause of Death',y='Total Number of Dead and Missing', color='Migration route',barmode='group',
            title="Number of Dead by Cause of Death")

    st.write(fig)
if len(route_input) > 0 and len(cause_of_death_input) > 0:
    plot_comp(route_input,cause_of_death_input,df2)
if len(route_input) > 0:
    for i in route_input:
        plot_deaths_season(i,df1)
        plot_deaths_cause(i,df2)


st.dataframe(df.head())

# TODO:
#  - make point larger based on number of dead
#  - filter based on:
#    - route
#    - gender
#    - region
