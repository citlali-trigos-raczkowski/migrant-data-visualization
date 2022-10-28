# migrant-data-visualization

## Parts 
Part 1: Visualize deaths of migrants in the Americas
Part 2: What are news sources saying about migrants on Twitter?

##  Work to be done:
- [x] Start a GH repository
- [x] Explore Data
    - [x] Take a look at the data 
    - [x] Some plots
- [ ] Pre-process
    - [x] Locations: check coordinates
    - [x] Seasons: transform dates to season 
    - [x] Null values/ missing
    - [x] Clustering for Data Points
    - [x] Outliers 
    - [ ] Data reliability
- [x] Visualizations
    - [x] Maps with coordinates 
    - [x] Group by location: death, numbers, seasons
- [x] Interaction: Display values on the coordinates
    - [x] Hover to show 
    - [x] Vary by season/location/type 
- [ ] ML idea: write an algorithm to search for statistics on migrants from reputable sources
    - [ ] download twitter api
    - [ ] Make list of words to search for
    - [ ] Identify what we want to narrow down to 
    - [ ] Look at the data of common words, see if we can extract something
- [x] Make a website: streamlit.io
    - [x] See how to embed the visualization into the website
    - [ ] Write a column to explain our project -- in progress
- [ ] Presentation 


# How to run the app.py script

Enter the src folder and run streamlit
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
