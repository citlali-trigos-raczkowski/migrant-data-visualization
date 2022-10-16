import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# Reference: Columns in our dataframe (migrantdf.columns):
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

# Prepare the Data

@st.cache
def get_data():
    url = data_url
    return pd.read_csv(url)


df = get_data()
df = df.rename(columns={"X": "lon", "Y": "lat"})
migrantdf = df

def get_df():
    '''Exports the full dataframe for use in other pages'''
    return df


# 0. Section for  Sidebar filters   *      *       *      *      *       *      *      *       *      *      *       *
# 0.1 Migration Route filter
st.sidebar.write("Data Filters")
route_input = st.sidebar.multiselect(
    'Migration Route', df['Migration route'].unique().tolist())
if len(route_input) > 0:
    migrantdf = migrantdf[migrantdf['Migration route'].isin(route_input)]
    show_route_death = True

# 0.2 Cause of death filter
cause_of_death_input = st.sidebar.multiselect(
    'Cause of Death', df['Cause of Death'].unique().tolist())
if len(cause_of_death_input) > 0:
    migrantdf = migrantdf[migrantdf['Cause of Death'].isin(
        cause_of_death_input)]


# 1.0 Introduction in Main Body  *      *       *      *      *       *      *      *       *      *      *       *
# 1.1 title and subtitle
st.title("Visualizing Deaths of Migrants at Borders")
st.markdown("Our team is working to understand and inform others about deaths of migrants, focused at borders. We are relying on the [Missing Migrants Project](https://missingmigrants.iom.int/) dataset, which includes data spanning from 2014 until 2022. This data includes incidents across the world, each dot on the map involving the death of 1 or more persons, with details about the location, cause of death, time, and more if it can be identified.  In this project, we use this data to create an interactive data visualization map of the world, allowing readers to see how migrant deaths vary by location, cause of death, gender, and season. Additionally, we enrich the project with more recent data from Twitter by filtering and pulling down Tweets about migrants.")
st.markdown("This migration data is more than just numbers. This is information about real people that left their home countries for various reasons and ultimately perished during their journey. This is data that requires respect and care in order to be presented faithfully. In this project, we aim to bring awareness to the challenges and risks that migrants face everyday. Perhaps you are familiar with several of the migration routes displayed here. There are likely other dangerous routes that you maybe haven't heard of. Many of us can recall certain newstories that made it to the news about the deaths of migrants, but as we can see in the data, this is an ongoing, everyday risk that affects many individuals, families, communitites, and countries around the world.")
st.markdown("We welcome you to explore the below visualization by zooming into the map directly or by using the filters in the left side menu.")

#map_w = folium.Map()
#loca = (migrantdf.iloc[0]['lon'],migrantdf.iloc[0]['lat'])
#custom_marker = folium.Marker(location=loca)
#custom_marker.add_to(map_w)
#st_map = st_folium(map_w)
# 1.2 map
#st.map(migrantdf)

fig = go.Figure(data=go.Scattergeo(
        lon = migrantdf['lon'],
        lat = migrantdf['lat'],
        text = migrantdf['Cause of Death Abbreviation'],
        #name=migrantdf['Migration route'],
        hoverinfo=['name','text',"lon+lat"],
        mode = 'markers',
        marker_color = 'rgb(210,30,0)',
        marker=dict(
            colorscale='Reds'
        )
        ))

fig.update_layout(
    title = 'Locations of the Reports',
    autosize=False,
    #width=750,
    #height=400,
    geo = dict(
        scope='world',
        showcountries = True,
        showocean = True,
        landcolor = "#f2f2f0",
        oceancolor = "#cad2d3",
        showcoastlines = False,
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
    )
    

st.plotly_chart(fig)
# 1.3 Route info
#Most common cause of death
#Total Number of deaths
#Total Number of Survivors

df_cause_of_death = df.groupby(['Migration route'])[
    'Cause of Death'].agg(pd.Series.mode).reset_index()
df_d_s = df.groupby(['Migration route'])[['Total Number of Dead and Missing','Number of Survivors']].sum().reset_index()

for route in route_input:
    st.subheader(f'Statistics for the route {route}')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric(f'Most common cause of death',df_cause_of_death[df_cause_of_death['Migration route'] == route]['Cause of Death Abbreviation'].iloc[0])
    with col2:
        st.metric(f'Total number of Dead and Missing',df_d_s[df_d_s['Migration route'] == route]['Total Number of Dead and Missing'].iloc[0])
    with col3:
        st.metric(f'Number of Survivors',df_d_s[df_d_s['Migration route'] == route]['Number of Survivors'].iloc[0])


#  1.4 Explore tabular data
st.header("Explore the Tabular Data")
# TODO: get these from the data (currently pulling directly from https://missingmigrants.iom.int/data)
total_no_deaths = df['Total Number of Dead and Missing'].sum()
total_med_deaths = df[df['Migration route'].isin(['Central Mediterranean','Western Mediterranean','Eastern Mediterranean'])]['Total Number of Dead and Missing'].sum()
total_drown_deaths = df[df['Cause of Death'].isin(['Drowning'])]['Total Number of Dead and Missing'].sum()

st.markdown("The data used in this project is collected and shared by the [Missing Migrants Project](https://missingmigrants.iom.int/). Each incident tracked by the project involves a migrant, refugee, or asylum-seeker who has died or gone missing while migrating across a border.")
st.markdown(" There have been over " + str(total_no_deaths) + " recorded deaths since 2014. The most deadly region is the Mediterranean, where at least " + str(total_med_deaths)+ " deaths have been recorded. The most common cause of death across the world is drowning, with at least " + str(total_drown_deaths) + " recorded deaths. All of these estimates are undercounts, as the project does not include counts of deaths of disappearances of migrants who have been established in a home, such as a refugee camp, or the deaths of persons who die within their country of origin while.")
st.markdown('From the Missing Migrant Project:\n "Missing Migrants Project data include the deaths of migrants who die in transportation accidents, shipwrecks, violent attacks, or due to medical complications during their journeys. It also includes the number of corpses found at border crossings that are categorized as the bodies of migrants, on the basis of belongings and/or the characteristics of the death. For instance, a death of an unidentified person might be included if the decedent is found without any identifying documentation in an area known to be on a migration route.  Deaths during migration may also be identified based on the cause of death, especially if is related to trafficking, smuggling, or means of travel such as on top of a train, in the back of a cargo truck, as a stowaway on a plane, in unseaworthy boats, or crossing a border fence.  While the location and cause of death can provide strong evidence that an unidentified decedent should be included in Missing Migrants Project data, this should always be evaluated in conjunction with migration history and trends."')
st.markdown('Explore the tabular data yourself using the filters in the left side menu.')
st.dataframe(migrantdf.head())

st.markdown('Interested to ')