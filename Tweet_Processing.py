"""
A script for processing tweets
"""

import numpy as np
import pandas as pd
import sklearn.feature_extraction.text as text
import matplotlib.pyplot as plt
import re
from collections import defaultdict

df1 = pd.read_csv("./data/sarw.csv")
df2 = pd.read_csv("./data/info.csv")
df3 = pd.read_csv("./data/uscg.csv")
df4 = pd.read_csv("./data/last_week.csv")

df = pd.concat([df1, df2, df3, df4])

tweetlist = df['Tweet'].tolist()

# delete links
for i in range(len(tweetlist)):
    tweetlist[i] = re.sub(r'https\S+', '', tweetlist[i])

    if tweetlist[i].startswith('RT'):
        tweetlist[i] = tweetlist[i][3:]

def ng(t_input, max_features, ngram):
    """
    Returns the top ngram words in a list of tweets.
    The aim is to see what words and word combinations appear to be the most common in the reports.
    

    Parameters
    ----------
    tweetlist : list
        A list of tweets
    max_features : int
        The maximum number of features to be used
    ngram : int
        The number of words to be used in the ngram

    Returns
    -------
    pd.Series
        A pandas series of the top ngram words in the list of tweets
    
    """
    tfidf = text.CountVectorizer(
        input = t_input, 
        ngram_range = (ngram, ngram),
        max_features = max_features,
        stop_words = 'english'
        )
    matrix = tfidf.fit_transform(t_input)
    
    return pd.Series(
        np.array(matrix.sum(axis = 0))[0],
        index = tfidf.get_feature_names_out()
        ).sort_values(ascending = False).head(100)

# printing the most common words and word combinations in the tweets to get an of what kind of wording is used in reports

unigrams = ng(
    t_input = tweetlist,
    max_features = 5000,
    ngram = 1
    )
bigrams = ng(
    t_input = tweetlist,
    max_features = 5000,
    ngram = 2
    )
trigrams = ng(
    t_input = tweetlist,
    max_features = 5000,
    ngram = 3
    )

print(unigrams.head(20))
print(bigrams.head(20))
print(trigrams.head(20))

print(df['Date'].head())
dm = []
dates = []
df2 = pd.DataFrame(columns = ['Date', 'Tweet'])

for tweet, date in zip(df['Tweet'], df['Date']):
    if 'migrant' in tweet or 'migrants' in tweet:
        if 'dead' in tweet or 'died' in tweet or 'death' in tweet or 'bodies' in tweet or 'missing' in tweet:
            dm.append(tweet)
            dates.append(date)
print(dm[0])
print(dates[0])

#for tweet in dm:
#    l = tweet.split()
#    for i in range(len(l)):
#        s = l[i].strip(',.:;')
#        st = ''
#        if s == 'dead' or s == 'died' or s == 'death' or s == 'bodies':
#            st += 'dead : ' + str(l[i-3]) + ' ' + str(l[i-2]) + ' ' + str(l[i-1]) + ' ' + str(l[i])
#        elif s == 'missing':
##            st += 'missing : ' + str(l[i-3]) + ' ' + str(l[i-2]) + ' ' + str(l[i-1]) + ' ' + str(l[i])
#        if st != '':
#            strs.append(st)

print(len(dm))
print(len(dates))
for t,d in zip(dm, dates):
    print('Tweet: ' + t + ' Date: ' + d)

# It appears to be very difficult to distiguish separate incidents since the reports do not include dates of occurence, and also 
# between incidents that occur migratory journeys and those that occur to migrants in general. The incidents are rare enough 
# that the amount of tweets after initial processing is only 95, and thus there is not enough return on investment to create a 
# language processing model to get the data, so instead I'll get data manually from the tweets.

data_list = [ 
    {'route' : 'Central Mediterranian', 'location' : 'Mahdia coast, Tunisia', 'number dead' : '15', 'number missing' : '0', 'date' : '2022-10-14'},
    {'route' : 'Central Mediterranian', 'location' : 'Trapani, Sicily', 'number dead' : '3', 'number missing' : '0', 'date' : '2022-10-13'},
    {'route' : 'Central Mediterranian', 'location' : 'Zarzis, Tunisia', 'number dead' : '11', 'number missing' : '0', 'date' : '2022-09-21'},
    {'route' : 'Central Mediterranian', 'location' : 'Sbaratha, Libya', 'number dead' : '15', 'number missing' : '0', 'date' : '2022-10-07'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Kythira, Greece', 'number dead' : '23', 'number missing' : '0', 'date' : '2022-10-05'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Lesbos', 'number dead' : '16', 'number missing' : '0', 'date' : '2022-10-06'},
    {'route' : 'Western Mediterranian', 'location' : 'Spain / Canary Islands', 'number dead' : '4', 'number missing' : '0', 'date' : '2022-10-06'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Syria', 'number dead' : '97', 'number missing' : '0', 'date' : '2022-09-26'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Aegean Sea, Turkey', 'number dead' : '6', 'number missing' : '0', 'date' : '2022-09-15'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Turkey, coast of Izmir', 'number dead' : '6', 'number missing' : '5', 'date' : '2022-09-15'},
    {'route' : 'Western Mediterranian', 'location' : 'Morocco', 'number dead' : '1', 'number missing' : '0', 'date' : '2022-09-13'},
    {'route' : 'Central Mediterranian', 'location' : 'Pozzallo, Sicily', 'number dead' : '6', 'number missing' : '0', 'date' : '2022-09-10'},
    {'route' : 'Central Mediterranian', 'location' : 'Tunisia', 'number dead' : '8', 'number missing' : '15', 'date' : '2022-09-09'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Crete, Greece', 'number dead' : '1', 'number missing' : '0', 'date' : '2022-09-08'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Lebanon', 'number dead' : '30', 'number missing' : '0', 'date' : '2022-04-24'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Turkey', 'number dead' : '1', 'number missing' : '0', 'date' : '2022-08-26'},
    {'route' : 'Western Mediterranian', 'location' : 'Canary Islands, Fuerteventura', 'number dead' : '3', 'number missing' : '0', 'date' : '2022-08-16'},
    {'route' : 'Central Mediterranian', 'location' : 'Libya, Sudan border', 'number dead' : '15', 'number missing' : '2', 'date' : '2022-08-15'},
    {'route' : 'Western Mediterranian', 'location' : 'Algerian coast', 'number dead' : '6', 'number missing' : '0', 'date' : '2022-08-09'},
    {'route' : 'Western Mediterranian', 'location' : 'Morocco, Akhfennir', 'number dead' : '8', 'number missing' : '0', 'date' : '2022-07-26'},
    {'route' : 'Sahara Desert crossing', 'location' : 'Niger, Libyan border', 'number dead' : '10', 'number missing' : '0', 'date' : '2022-07-01'},
    {'route' : 'Central Mediterranian', 'location' : 'Calabrian coast', 'number dead' : '5', 'number missing' : '0', 'date' : '2022-07-25'},
    {'route' : 'Sahara Desert crossing', 'location' : 'Libya, Chad border', 'number dead' : '20', 'number missing' : '0', 'date' : '2022-06-30'},
    {'route' : 'Central Mediterranian', 'location' : 'Central Mediterranian', 'number dead' : '0', 'number missing' : '30', 'date' : '2022-06-27'},
    {'route' : 'US-Mexico border crossing', 'location' : 'US, San Antonio', 'number dead' : '46', 'number missing' : '0', 'date' : '2022-06-28'},
    {'route' : 'Central Mediterranian', 'location' : 'Morocco (to Mellilla)', 'number dead' : '23', 'number missing' : '0', 'date' : '2022-06-28'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Lesbos, Greece', 'number dead' : '2', 'number missing' : '0', 'date' : '2022-06-27'},
    {'route' : 'Central Mediterranian', 'location' : 'Tunisia, Coast of Sfax', 'number dead' : '16', 'number missing' : '0', 'date' : '2022-06-21'},
    {'route' : 'Eastern Mediterranian', 'location' : 'Greece, Aegean sea', 'number dead' : '0', 'number missing' : '8', 'date' : '2022-06-20'},
    {'route' : 'Western Mediterranian', 'location' : 'Spain coast', 'number dead' : '4', 'number missing' : '0', 'date' : '2022-06-09'},
    {'route' : 'Caribbean to US', 'location' : 'Ilsa Morada', 'number dead' : '0', 'number missing' : '1', 'date' : '2022-09-02'}]

s = defaultdict(int)

# counts for each route
for d in data_list:
    string = d['route']
    s[string] += 1

print(s)

dataframe = pd.DataFrame.from_dict(data_list)
print(dataframe.head())

# save dataframe to csv
#dataframe.to_csv('data.csv', index=False)
