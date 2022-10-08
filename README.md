# migrant-data-visualization

## Parts 
Part 1: Visualize deaths of migrants in the Americas
Part 2: What are news sources saying about migrants on Twitter?

##  Work to be done:
- [x] Start a GH repository
- [ ] Explore Data
    - [ ] Take a look at the data 
    - [ ] Some plots
- [ ] Pre-process
    - [ ] Locations: check coordinates
    - [ ] Seasons: transform dates to season 
    - [ ] Null values/ missing
    - [ ] Outliers 
    - [ ] Data reliability
- [ ] Visualizations
    - [ ] Maps with coordinates 
    - [ ] Group by location: death, numbers, seasons
- [ ] Interaction: Display values on the coordinates
    - [ ] Hover to show 
    - [ ] Vary by season/location/type 
- [ ] ML idea: write an algorithm to search for statistics on migrants from reputable sources
    - [ ] download twitter api
    - [ ] Make list of words to search for
    - [ ] Identify what we want to narrow down to 
    - [ ] Look at the data of common words, see if we can extract something
- [ ] Make a website: streamlit.io
    - [ ] See how to embed the visualization into the website
    - [ ] Write a column to explain our project 
- [ ] Presentation 


# How to run the app.py script

Enter the scripts folder and run streamlit
```
cd scripts/
streamlit run app.py
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