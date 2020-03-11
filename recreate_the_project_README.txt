In order to recreate this project. 

##imports:

pandas as pd
pymongo

from unique_list ...UniqueList
from convert ...ListConverter

##initalize and define the database:

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.peep_tweets_db
collection = db.tweets

##perform the following transformations:

df_visitors = pd.read_csv('wh_visitor_logs.csv')
visitors = df_visitors["Attendees"]
visitors = visitors.dropna(how='any')
visitors_df = pd.DataFrame(visitors) 
named_visitors = visitors_df.loc[visitors_df["Attendees"] != "(b)(6)", :]
visitors_df2 = named_visitors["Attendees"].str.split(",", n=13, expand = True)
visitors_df3 = named_visitors["Attendees"].str.split(",", n=2, expand = True)
del visitors_df3[1]
del visitors_df3[2]
visitors_df3.rename(columns={0 :'name'}, inplace=True )
visitors_df3.set_index('name')
visitors_df3.drop_duplicates(keep=False, inplace=True)
#
df_cats = pd.read_csv('fatcats.csv')
del df_cats['id']
del df_cats['blurb']
del df_cats['types']
df_cats.set_index('name')
df_lobs = pd.read_csv('lobbyists.csv')
del df_lobs['id']
del df_lobs['blurb']
del df_lobs['types']
df_lobs.set_index('name')
df_catslobs = df_cats.append(df_lobs, ignore_index=True)
df_catslobs.set_index('name')
df_catslobs.drop_duplicates(keep=False, inplace=True)
#
df_peeps = df_catslobs.append(visitors_df3, ignore_index=True)
df_peeps.set_index('name')
df_peeps.drop_duplicates(keep=False, inplace=True)

#initiate and utilize custom classes:

job = UniqueList()
peeps = job.make_list_from_df(df_peeps,'name')
tweets = job.make_list_from_csv('archive_test.csv', 'text')
conversion = ListConverter()
peep_tweets = conversion.associate(peeps, tweets)
post = peep_tweets

# add object to database

collection.insert_one(post)

A comprehensive and commented run through of the project can be see on the ETL Project.ipynb file.