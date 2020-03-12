#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pymongo


# In[2]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[3]:


# Define database and collection
db = client.peep_tweets_db
collection = db.tweets


# In[4]:


# Ryan's work

# Read in csv
df_visitors = pd.read_csv('wh_visitor_logs.csv')
visitors = df_visitors["Attendees"]

# Drop NaN values
visitors = visitors.dropna(how='any')
visitors_df = pd.DataFrame(visitors) 

# Drop redacted - (b)(6) - visitors
named_visitors = visitors_df.loc[visitors_df["Attendees"] != "(b)(6)", :]

# Explode attendee column
visitors_df2 = named_visitors["Attendees"].str.split(",", n=13, expand = True)
visitors_df3 = named_visitors["Attendees"].str.split(",", n=2, expand = True)

# Retain only first visitor
del visitors_df3[1]
del visitors_df3[2]
visitors_df3.rename(columns={0 :'name'}, inplace=True )
visitors_df3.set_index('name')

# Delete any duplicate visitors
visitors_df3.drop_duplicates(keep=False, inplace=True)
visitors_df3


# In[5]:


# Ryan's work

# Read in csv 
df_cats = pd.read_csv('fatcats.csv')

# Remove unnecessary variables and set index
del df_cats['id']
del df_cats['blurb']
del df_cats['types']
df_cats.set_index('name')

# Read in csv
df_lobs = pd.read_csv('lobbyists.csv')

# Remove unnecessary variables and set index
del df_lobs['id']
del df_lobs['blurb']
del df_lobs['types']
df_lobs.set_index('name')

# Append lobbyist list to fat cat list and ensure no duplicates
df_catslobs = df_cats.append(df_lobs, ignore_index=True)
df_catslobs.set_index('name')
df_catslobs.drop_duplicates(keep=False, inplace=True)
df_catslobs

# Append visitors list to catslobs list and ensure no duplicates
df_peeps = df_catslobs.append(visitors_df3, ignore_index=True)
df_peeps.set_index('name')
df_peeps.drop_duplicates(keep=False, inplace=True)
df_peeps


# In[6]:


# comprehensive comments on classes are in Philip_README.txt 
from unique_list import UniqueList
from convert import ListConverter


# In[7]:


job = UniqueList()
# initiate an instance of the UniqueList class
peeps = job.make_list_from_df(df_peeps,'name')
# call the make list from df method which takes a dataframe and a column and returns a list of names


# In[8]:


tweets = job.make_list_from_csv('archive_test.csv', 'text')
# call the make list from csv method which takes a csv and column and returns a list of tweets


# In[9]:


conversion = ListConverter()
# initiate the ListConverter class


# In[10]:


peep_tweets = conversion.associate(peeps, tweets)
# call the assosiate method which takes two lists returns a dictionary


# In[11]:


conversion.get_keys(peep_tweets)
# call the get keys method which gives all keys (cases in which the script found a tweet(s) to assosiate with a 
# name) ultimately to check that our script worked


# In[12]:


# Dictionary to be inserted as a MongoDB document
post = peep_tweets
collection.insert_one(post)


# In[13]:


# Display the MongoDB records created above
tweet = db.tweets.find()
for tweet in tweets:
    print(tweet)


# In[ ]:




