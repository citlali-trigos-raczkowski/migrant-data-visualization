import geopandas as gpd
import streamlit as st
import pandas as pd
from shapely.geometry import Point

df = pd.read_csv('Missing_Migrants_Global_Figures_allData.csv')

df2 = df[['Migration route','Coordinates']]

geometry = [Point(xy) for xy in zip(df.X, df.Y)]

gdf = gpd.GeoDataFrame(df2, crs="EPSG:4326", geometry=geometry)

fig = gdf.explore()

st.plotly_chart(fig, use_container_width=True)
