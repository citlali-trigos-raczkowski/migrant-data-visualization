import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from millify import prettify

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

year_input = st.sidebar.multiselect('Year',
                                    df['Incident year'].unique().tolist())
if len(year_input) > 0:
    year_input.sort()
    migrantdf = migrantdf[migrantdf['Incident year'].isin(
        year_input)]

# 1.0 Introduction in Main Body  *      *       *      *      *       *      *      *       *      *      *       *
# 1.1 title and subtitle
st.title("Visualizing Deaths of Migrants at Borders")
st.markdown("Our team is working to understand and inform others about deaths of migrants, focused at borders. We are relying on the [Missing Migrants Project](https://missingmigrants.iom.int/) dataset, which includes data from 2014 to 2022. This data includes incidents across the world, each dot on the map representing the death of 1 or more persons, with details about the location, cause of death, time, and more, if it can be identified.  In this project, we use this data to create an interactive data visualization map of the world, allowing readers to see how migrant deaths vary by location, cause of death, gender, and season.")
st.markdown("The lastest entries in the data we used from the Missing Migrants Project spans until August 2022. To highlight that the occurrence of these tragedies is an ongoing phenomenon, we wanted to add newer data from the most recent reports to our dataset. We achieved this by pulling Tweets from different sources of news reports on Twitter using the Twitter API. This part can be found from the Twitter page in the sidebar.")
st.markdown("This migration data is more than just numbers. This is information about real people that left their home countries for various reasons and ultimately perished during their journey. This is data that requires respect and care in order to be presented faithfully. In this project, we aim to bring awareness to the challenges and risks that migrants and their loved ones face everyday. Perhaps you are familiar with several of the migration routes displayed here. There are likely other dangerous routes that you haven't heard of. Many of us can recall certain stories that made it to the news about the deaths of migrants, but as we can see in the data, this is an ongoing, everyday risk that affects many individuals, families, communitites, and countries around the world.")
st.markdown("We welcome you to explore the below visualization by zooming into the map directly or by using the filters in the left side menu.")

# 1.2 Global Statistics
# st.markdown(str(year_input), str(len(year_input)))
if len(year_input) == 1:
    year_text = " in " + str(year_input[0])
elif len(year_input) == 2:
    year_text = " in " + str(year_input[0]) + ' and ' + str(year_input[1])
elif len(year_input) > 2:
    year_text = " in " + str(year_input[0])
    for year in year_input[1:-1]:
        year_text += ', ' + str(year)
    year_text += ', and ' + str(year_input[-1])
else:
    year_text = ''

if len(year_input) > 0:
    statsdf = df[df['Incident year'].isin(
        year_input)]
else:
    statsdf = df
df_cause_of_death = statsdf.groupby('Cause of Death Abbreviation')['Cause of Death Abbreviation', 'Total Number of Dead and Missing'].sum(
).sort_values('Total Number of Dead and Missing', ascending=False).reset_index()
df_cause_of_death['Total Number of Dead and Missing'] = df_cause_of_death['Total Number of Dead and Missing'].apply(
    lambda x: prettify(x))

st.subheader(f'Global Statistics' + str(year_text))
st.markdown(f'Most common causes of death')
st.dataframe(df_cause_of_death, height=200)

col2, col3 = st.columns(2)
with col2:
    st.metric(f'Total number of Recorded Dead and Missing',
              prettify(statsdf['Total Number of Dead and Missing'].sum()))
with col3:
    st.metric(f'Total Number of Recorded Survivors',
              prettify(statsdf['Number of Survivors'].sum()))

# 1.3 Display the map
fig = go.Figure(data=go.Scattergeo(
    lon=migrantdf['lon'],
    lat=migrantdf['lat'],
    text=migrantdf['Cause of Death Abbreviation'],
    #hoverlabel=migrantdf['Migration route'],
    hoverinfo=['text'],
    mode='markers',
    marker_color='rgb(210,30,0)',
    marker=dict(
        colorscale='Reds'
    )
))

fig.update_layout(
    title='Locations of the Reports',
    autosize=False,
    # width=750,
    # height=400,
    geo=dict(
        scope='world',
        showcountries=True,
        showocean=True,
        landcolor="#f2f2f0",
        oceancolor="#cad2d3",
        showcoastlines=False,
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
)

# changing column names for the hovering capability
plotdf = migrantdf[['lat', 'lon']]
plotdf['Migration Route'] = migrantdf['Migration route']
plotdf['Cause of Death'] = migrantdf['Cause of Death Abbreviation']
plotdf['Year'] = migrantdf['Incident year']
plotdf['People Dead/Missing'] = migrantdf['Total Number of Dead and Missing']

plot = px.scatter_geo(plotdf, lat='lat', lon='lon',
                      hover_name='Migration Route',
                      hover_data={'Cause of Death': True,
                                  'People Dead/Missing': True,
                                  'Year': True,
                                  'lon': False,
                                  'lat': False
                                  },
                      color_discrete_sequence=['red']
                      )

plot.update_layout(
    title='Locations of the Reports',
    autosize=False,
    # width=750,
    # height=400,
    geo=dict(
        scope='world',
        showcountries=True,
        showocean=True,
        landcolor="#f2f2f0",
        oceancolor="#cad2d3",
        showcoastlines=False,
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
)

st.header("Explore the World Map")
st.markdown("When you hover over the graph with your mouse, you'll see additional data appear. Each dot on the graph marks a single incident, and the tooltip for that dot gives data on: (1) Cause of Death, (2) How many total people died or went missing for the incident, and (3) Which year the incident occured in.")
st.markdown("The map can be made full-screen. When you hover over the map, a menu should appear above it. The right-most arrows, when selected, will make the map full screen.")
st.plotly_chart(plot)

#  1.4 Explore tabular data
st.header("Explore the Tabular Data")
total_no_deaths = prettify(df['Total Number of Dead and Missing'].sum())
total_med_deaths = prettify(df[df['Migration route'].isin(
    ['Central Mediterranean', 'Western Mediterranean', 'Eastern Mediterranean'])]['Total Number of Dead and Missing'].sum())
total_drown_deaths = prettify(df[df['Cause of Death'].isin(
    ['Drowning'])]['Total Number of Dead and Missing'].sum())

st.markdown(
    "The data used in this project is collected and shared by the [Missing Migrants Project](https://missingmigrants.iom.int/). Each incident tracked by the project involves a migrant, refugee, or asylum-seeker who has died or gone missing while migrating across a border.")
st.markdown(" There have been over " + total_no_deaths + " recorded deaths since 2014. The **most deadly region is the Mediterranean**, where at least " + total_med_deaths + " deaths have been recorded. The most common **cause of death** across the world is drowning, with at least " +
            total_drown_deaths + " recorded deaths.")
st.markdown("All of these estimates are undercounts, as the project does not include counts of deaths of disappearances of migrants who have been established in a home, such as a refugee camp, or the deaths of persons who die within their country of origin while.")
st.markdown('From the Missing Migrant Project:\n\n *"Missing Migrants Project data include the deaths of migrants who die in transportation accidents, shipwrecks, violent attacks, or due to medical complications during their journeys. It also includes the number of corpses found at border crossings that are categorized as the bodies of migrants, on the basis of belongings and/or the characteristics of the death. For instance, a death of an unidentified person might be included if the decedent is found without any identifying documentation in an area known to be on a migration route.  Deaths during migration may also be identified based on the cause of death, especially if is related to trafficking, smuggling, or means of travel such as on top of a train, in the back of a cargo truck, as a stowaway on a plane, in unseaworthy boats, or crossing a border fence.  While the location and cause of death can provide strong evidence that an unidentified decedent should be included in Missing Migrants Project data, this should always be evaluated in conjunction with migration history and trends."*')
st.markdown(
    'Explore the tabular data yourself using the filters in the left side menu.')
st.dataframe(migrantdf)
