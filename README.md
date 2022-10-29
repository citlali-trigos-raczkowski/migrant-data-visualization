# Visualizing Deaths of Migrants at Borders

Check out the [deployed application here.](https://citlali-trigos-raczkowski-migrant-data-visualiza-srchome-b0llv8.streamlitapp.com/)

## Introduction

This project was created to try to understand and inform others about the deaths of migrants, focused at borders. It relies on the [Missing Migrants Project](https://missingmigrants.iom.int/) dataset, which includes data from 2014 to 2022. This data includes incidents across the world, each entry representing the death of 1 or more persons, with details about the location, cause of death, time, and more, if it can be identified.

In this project, the data is used to create an interactive data visualization map of the world, allowing readers to see how migrant deaths vary by location, cause of death, gender, and season. To highlight that the occurrence of these tragedies is an ongoing phenomenon, we wanted to add newer data from the most recent reports to our dataset. We achieved this by pulling Tweets from different sources of news reports on Twitter using the Twitter API. This part can be found from the Twitter page of the application.

## Streamlit Application

This application is built and deployed using [Streamlit.io](https://streamlit.io/). The data displayed in the application is csv data downloaded from the [Missing Migrants Project](https://missingmigrants.iom.int/) and by filtering through the [Twitter API](https://developer.twitter.com/en/docs/twitter-api).

The project is written in python, but exploratory data analysis are written in Jupyter notebooks (which can be found in the [exploration](./exploration/) folder).

We use the following libraries:

- [streamlit](https://streamlit.io/), the framework for the application
- [pandas](https://pandas.pydata.org/), to explore and manipulate the CSV dataframes
- [plotly](https://plotly.com/), to create the interactive map
- [millify](https://www.npmjs.com/package/millify), to make the numbers readable (`1220098` --> `1,220,098`)

## Running this repo locally

The above packages will all need to be installed before being able to view the application.

To start the application, run the following from the root:

```
streamlit run src/Home.py
```

If the command streamlit is not found, then you're going to need to first [set up streamlit](https://docs.streamlit.io/library/get-started/installation). I'm using a conda virtual environment

After running the above command, you should see this in your terminal shell:

```
(geo_env) ➜  scripts git:(main) ✗ streamlit run app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.101.106:8501

```

And you'll be able to access the streamlit app in your browser.

Here's a file I found useful of how to use various streamlit-markdown commands: [gh-file](https://github.com/shaildeliwala/experiments/blob/master/streamlit.py)

test
