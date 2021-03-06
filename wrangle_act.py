#!/usr/bin/env python
# coding: utf-8

# # Gathering Data

# In[1]:


import tweepy
from tweepy import OAuthHandler
import json
from timeit import default_timer as timer
import pandas as pd
import numpy as np
import requests
import os 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[2]:


# read csv file.
df = pd.read_csv('twitter-archive-enhanced.csv')


# In[3]:


# create copy of df.
df_doggo = df.copy()


# In[4]:


df_doggo.head()


# In[5]:


# Programmatically download file from website.
response = requests.get("https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv")
with open('image-predictions.tsv', mode='wb') as file:
    file.write(response.content)


# In[6]:


df_i = pd.read_csv('image-predictions.tsv', sep='\t')


# In[7]:


# Make a copy of df_i.
df_image = df_i.copy()


# In[8]:


# Query Twitter API for each tweet in the Twitter archive and save JSON in a text file
# These are hidden to comply with Twitter's API terms and conditions
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# NOTE TO STUDENT WITH MOBILE VERIFICATION ISSUES:
# df_1 is a DataFrame with the twitter_archive_enhanced.csv file. You may have to
# change line 17 to match the name of your DataFrame with twitter_archive_enhanced.csv
# NOTE TO REVIEWER: this student had mobile verification issues so the following
# Twitter API code was sent to this student from a Udacity instructor
# Tweet IDs for which to gather additional data via Twitter's API
tweet_ids = df.tweet_id.values
len(tweet_ids)

# Query Twitter's API for JSON data for each tweet ID in the Twitter archive
count = 0
fails_dict = {}
start = timer()
# Save each tweet's returned JSON as a new line in a .txt file
with open('tweet_json.txt', 'w') as outfile:
    # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
    for tweet_id in tweet_ids:
        count += 1
        print(str(count) + ": " + str(tweet_id))
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            print("Success")
            json.dump(tweet._json, outfile)
            outfile.write('\n')
        except tweepy.TweepError as e:
            print("Fail")
            fails_dict[tweet_id] = e
            pass
end = timer()
print(end - start)
print(fails_dict)


# In[9]:


# Create new dataframe with id, retweet_count, and favorite_count.

tweet_json = open('tweet_json.txt', 'r')
df_tweet = pd.DataFrame(columns=['tweet_id', 'retweets', 'favorites'])

for line in tweet_json:
    tweet = json.loads(line)
    df_tweet = df_tweet.append({'tweet_id': tweet['id'], 'retweets': tweet['retweet_count'], 'favorites': tweet['favorite_count']}, ignore_index=True)
tweet_json.close()

df_tweet


# In[10]:


# Make a copy of df_tweet.
df_tweet_data = df_tweet.copy()


# # Assessing Data

# In[11]:


# Check data types are compatible and columns are not missing entries.
df_doggo.info()


# In[12]:


# Check data types are compatible and columns are not missing entries.
df_image.info()


# In[13]:


# Check data types are compatible and columns are not missing entries.
df_tweet_data.info()


# In[14]:


# Make sure numerators are consistent.
df_doggo.rating_numerator.unique()


# In[15]:


# Check for any numerators that equal zero.
df_doggo[df_doggo.rating_numerator == 0]


# In[16]:


# Make sure denominators are consistent
df_doggo.rating_denominator.unique()


# In[17]:


# Check for any denominators that equal zero.
df_doggo[df_doggo.rating_denominator == 0]


# In[18]:


# Detect entries where there are more than one dog stage.
df_doggo.loc[(df_doggo[['doggo', 'floofer', 'pupper', 'puppo']] != 'None').sum(axis=1) > 1]


# In[19]:


# Convert all entries in df_tweet_data to integer to help assess data further.
df_tweet_data = df_tweet_data.astype(str).astype(int)


# In[20]:


# Check if there are any favorite entries that equal zero.
df_tweet_data[df_tweet_data['favorites'] == 0]


# In[21]:


# Check if there are more retweets than favorites for a tweet (as this is unusual)
df_tweet_data[df_tweet_data['retweets'] > df_tweet_data['favorites']]


# In[22]:


# See if there are any duplicates in the data frame.
sum(df_tweet_data.duplicated())


# In[23]:


# See if there are any duplicates in the data frame.
sum(df_image.duplicated())


# In[24]:


# See if there are any dupulicates in the data frame.
sum(df_doggo.duplicated())


# ## Detect and document at least eight (8) quality issues and two (2) tidiness issues
# Quality issue dimensions are:
# 1. `Completeness`: do we have all of the records that we should? Do we have missing records or not? Are there specific rows, columns, or cells missing?
# 2. `Validity`: we have the records, but they’re not valid, i.e., they don’t conform to a defined schema. A schema is a defined set of rules for data. These rules can be real-world constraints (e.g. negative height is impossible) and table-specific constraints (e.g. unique key constraints in tables).
# 3. `Accuracy`: inaccurate data is wrong data that is valid. It adheres to the defined schema, but it is still incorrect. Example: a patient’s weight that is 5 lbs too heavy because the scale was faulty.
# 4. `Consistency`: inconsistent data is both valid and accurate, but there are multiple correct ways of referring to the same thing. Consistency, i.e., a standard format, in columns that represent the same data across tables and/or within tables is desired.
# 
# Tidy Data requirements:
# 1. Each variable forms a column.
# 2. Each observation forms a row.
# 3. Each type of observational unit forms a table.
# 
# ### Quality Issues
# 
# 1. Missing values for dog stage (incomplete data for doggo, floofer, pupper, puppo) in `df_doggo`.
# 2. Multiple values for dog stage in `df_doggo`.
# 3. Rating numerators and  rating denominators values are incorrect in `df_doggo`.
# 4. Remove entries that are retweets in `df_doggo`.
# 5. Replace 'None' with 'NaN' for all dog stages in `df_doggo`.
# 6. Columns pertaining to retweets and expanded URLs are unnecessary in `df_doggo`.
# 7. Remove entries where p1_dog, p2_dog, and p3_dog are all "False" in `df_image`.
# 8. Values for p1, p2, and p3 sometimes capitalized but not always in `df_image`.
# 9. All columns in `df_tweet_data` should be integers.
# 10. 167 rows missing data for `favorites` in `df_tweet_data`.
# 
# 
# ### Tidiness Issues
# 1. Doggo, floofer, pupper, puppo are one variable spread across different columns in `df_doggo`. 
# 2. rating_numerator and rating_denominator can be combined into one column in `df_doggo`.
# 3. Combine data frames by tweet_id.
# 

# # Cleaning Data

# ## Quality Issues

# ### 1. Missing values for dog stage (incomplete data for `doggo`, `floofer`, `pupper`, `puppo`) in `df_doggo`.
# - Remove rows that contain "None" values for all dog stages.

# #### Code

# In[25]:


df_doggo_1 = df_doggo.query('doggo != "None" or floofer != "None" or pupper != "None" or puppo != "None"')


# #### Test

# In[26]:


df_doggo_1


# ### 2. Multiple values for dog stage in `df_doggo`.

# - Remove rows that contain multiple values for all dog stages.

# #### Code

# In[27]:


# Remove entries where there are more than one dog stage
df_doggo_1 = df_doggo_1.loc[(df_doggo_1[['doggo', 'floofer', 'pupper', 'puppo']] != 'None').sum(axis=1) == 1]


# #### Test

# In[28]:


df_doggo_1.loc[(df_doggo_1[['doggo', 'floofer', 'pupper', 'puppo']] != 'None').sum(axis=1) > 1]


# ### 3. `rating_numerators` and  `rating_denominator` values are incorrect in `df_doggo`.

# #### Code

# In[29]:


df_doggo_1['rating_denominator'].unique()


# In[30]:


df_doggo_1['rating_numerator'].unique()


# In[31]:


df_doggo_1['rating_numerator'] = df_doggo_1.text.str.extract('((?:\d+\.)?\d+)\/(\d+)', expand=True)


# In[32]:


df_doggo_1['rating_numerator'] = df_doggo_1['rating_numerator'].astype(str).astype(float)


# In[33]:


df_doggo_1['rating_denominator'] = df_doggo_1['rating_denominator'].astype(str).astype(float)


# #### Test

# In[34]:


df_doggo_1['rating_denominator'].unique()


# In[35]:


df_doggo_1['rating_numerator'].unique()


# In[36]:


# Make sure that numerator and denominator are in compatible format
df_doggo_1['rating_numerator'] / df_doggo_1['rating_denominator']


# ### 4. Remove entries that are retweets in `df_doggo`.

# #### Code

# In[37]:


df_doggo_2 = df_doggo_1.query('retweeted_status_id == "NaN"')


# #### Test

# In[38]:


# Test to see if retweet columns contain any values.

df_doggo_2.info()


# ### 5. Replace 'None' with 'NaN' for all dog stages in `df_doggo`.

# #### Code

# In[39]:


df_doggo_2['doggo'] = np.where(df_doggo_2['doggo'] == 'None' , np.nan, df_doggo_2['doggo'])
df_doggo_2['floofer'] = np.where(df_doggo_2['floofer'] == 'None' , np.nan, df_doggo_2['floofer'])
df_doggo_2['pupper'] = np.where(df_doggo_2['pupper'] == 'None' , np.nan, df_doggo_2['pupper'])
df_doggo_2['puppo'] = np.where(df_doggo_2['puppo'] == 'None' , np.nan, df_doggo_2['puppo'])


# #### Test

# In[40]:


df_doggo_2


# ### 6. Columns pertaining to retweets and expanded URLs are unnecessary in df_doggo.

# #### Code

# In[41]:


df_doggo_2.drop(columns=['retweeted_status_id','retweeted_status_user_id', 'retweeted_status_timestamp', 'expanded_urls', 'source'], inplace=True)


# #### Test

# In[42]:


df_doggo_2


# ### 7. Remove entries where `p1_dog`, `p2_dog`, and `p3_dog` are all "False" in `df_image`.

# #### Code

# In[43]:


df_image_1 = df_image.query('p1_dog == True or p2_dog == True or p3_dog == True')


# #### Test

# In[44]:


df_image_1.query('p1_dog == False & p2_dog == False & p3_dog == False')


# ### 8. Values for p1, p2, and p3 sometimes capitalized but not always in df_image.

# #### Code

# In[45]:


df_image_1.p1.str.lower()


# #### Test

# In[46]:


df_image_1


# ### 9. All columns in df_tweet_data should be integers.
# - This was completed while assessing data in order to properly assess the data.

# #### Code

# df_tweet_data was converted to an integer in the Assess Data section using the following code:
# `df_tweet_data = df_tweet_data.astype(str).astype(int)`

# #### Test

# In[47]:


df_tweet_data.info()


# ### 10. 167 rows missing data for `favorites` in `df_tweet_data`.

# #### Code

# In[48]:


df_tweet_data_1 = df_tweet_data.query('favorites != "0"')


# #### Test

# In[49]:


df_tweet_data_1.query('favorites == "0"')


# ## Tidiness Issues

# ### 1. Doggo, floofer, pupper, puppo are one variable spread across different columns in df_doggo.

# #### Code

# In[50]:


df_doggo_2['doggo'] = df_doggo_2['doggo'].fillna(df_doggo_2['floofer'])
df_doggo_2['doggo'] = df_doggo_2['doggo'].fillna(df_doggo_2['pupper'])
df_doggo_2['doggo'] = df_doggo_2['doggo'].fillna(df_doggo_2['puppo'])
df_doggo_2.drop(columns=['floofer','pupper', 'puppo'], inplace=True)
df_doggo_2


# In[51]:


df_doggo_2 = df_doggo_2.rename(index=str, columns={"doggo": "dog_stages"})


# #### Test

# In[52]:


df_doggo_2


# ### 2. rating_numerator and rating_denominator can be combined into one column in `df_doggo`.

# #### Code

# In[53]:


df_doggo_2['rating_percent'] = df_doggo_2.rating_numerator/df_doggo_2.rating_denominator
df_doggo_2


# In[54]:


df_doggo_2.drop(columns=['rating_numerator','rating_denominator'], inplace=True)


# #### Test

# In[55]:


df_doggo_2


# ### 3. Combine dataframes by tweet_id

# In[56]:


df_merge = pd.merge(df_image_1, df_doggo_2, on=['tweet_id'])
df_merge


# In[57]:


df_merge = pd.merge(df_merge, df_tweet_data_1, on=['tweet_id'])
df_merge


# ## Store the clean DataFrame in a CSV file

# In[58]:


df_merge.to_csv('twitter_archive_master.csv', index=False)


# ## Insights

# #### 1. p1 predicts that it is a dog 87% of the time.

# In[59]:


df_merge.p1_dog.mean()


# #### 2. Number of Favorites for each Dog Stage.

# In[60]:


df_merge.groupby(['dog_stages'])['favorites'].mean()


# #### 3. Number of Retweets for each Dog Stage

# In[61]:


df_merge.groupby(['dog_stages'])['retweets'].mean()


# ## Visualize the Data

# #### 1. Average Rating Percent for each Dog Stage

# In[62]:


# calculate mean ratings by dog stage
stage_rating_avg = df_merge.groupby(['dog_stages'])['rating_percent'].mean()


# In[63]:


# convert series to a data frame
stage_rating_avg.to_frame()


# In[64]:


stage_rating_avg1 = stage_rating_avg.reset_index(level=['dog_stages'])
stage_rating_avg1.sort_values(by='rating_percent', ascending=False)


# In[65]:


g = sns.barplot(data=stage_rating_avg1, x="dog_stages", y="rating_percent")
g.set_xticklabels(g.get_xticklabels(), rotation=90)
ax = plt.gca()
ax.set_title("Average Rating Percent by Dog Stage")
plt.xlabel("Dog Stages")
plt.ylabel("Average Rating Percent")


# According to the barplot above, the average rating percent ranking for each dog stage is as follows:
# 1. floofer
# 2. puppo
# 3. doggo
# 4. pupper
