import streamlit as st
import pandas as pd

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
route_input = st.sidebar.multiselect('Migration Route', df.groupby(
    'Migration route').count().reset_index()['Migration route'].tolist())
if len(route_input) > 0:
    migrantdf = df[df['Migration route'].isin(route_input)]

# 3. Add filter by cause of death to sidebar
cause_of_death_input = st.sidebar.multiselect('Cause of Death', df.groupby(
    'Cause of Death').count().reset_index()['Cause of Death'].tolist())
if len(cause_of_death_input) > 0:
    migrantdf = df[df['Cause of Death'].isin(cause_of_death_input)]

st.map(migrantdf)

st.markdown("Data for the above visualization can be explored below:")

st.dataframe(df.head())

# TODO:
#  - make point larger based on number of dead
#  - filter based on:
#    - route
#    - gender
#    - region
