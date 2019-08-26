# Wrangle-analyze-twitter-posts

## Wrangle and Visualize Twitter Posts
Wrangle the data, analyze the data, and visualize a tweet archive dataset.

## Description
The dataset is the tweet archive of Twitter user @dog_rates, also known as WeRateDogs. WeRateDogs is a Twitter account that rates people's dogs with a humorous comment about the dog. These ratings almost always have a denominator of 10. The numerators, though? Almost always greater than 10. 11/10, 12/10, 13/10, etc. Why? Because "they're good dogs Brent." WeRateDogs has over 4 million followers and has received international media coverage. My task is to wrangle the data, analyze the data, and visualize the data.

## Getting Started
### Dependencies
- Windows 10
- Python 3

### Libraries
- tweepy
- json
- timeit 
- pandas
- numpy
- requests
- os 
- matplotlib
- seaborn

## Findings
### p1 predicts that the tweet image is a dog 87% of the time.
I used the Pandas `.mean()` function to find out how often the neural network was able to predict a breed of
dog based on a tweet image for its first prediction. The function revealed that the neural network was able
to do this 87% of the time. This means that 13% of neural network’s first predictions were not a breed of
dog. Perhaps this is something that can be improved in the future so that the first predictions are able to
predict dog breed with better accuracy.
### Number of Favorites for each Dog Stage.
I used the Pandas `.groupby().mean()` function to find out which dog stage yielded the most favorites on
average. The ‘puppo’ dog stage yielded the most favorites on average (approximately 21,577 per tweet),
followed by ‘doggo’ (approximately 20,242 favorites per tweet), followed by ‘floofer’ (approximately 12,581
favorites per tweet), followed by ‘pupper’ (approximately 7,276 favorites per tweet).
### Number of Retweets for each Dog Stage
I used the Pandas `.groupby().mean()` function to find out which dog stage yielded the most retweets. This
time the ‘doggo’ stage yielded the most retweets on average (approximately 7,001 retweets per tweet),
followed by ‘puppo’ (approximately 6,143 retweets per tweet), followed by ‘floofer’ (approximately 4,641
retweets per tweet), followed by ‘pupper’ (approximately 2,281 retweets per tweet).

### Visualizing the data
#### Average Rating Percent for each Dog Stage
I used the Pandas `.groupby().mean()` function to calculate the mean rating percent by dog stage and then
converted the series to a data frame by using the Pandas `.to_frame() function. I used Pandas `reset_index()` function to convert dog_stages from index to column and then used `.sort_values()` to order
the dog stages by descending rating percent values.

I then plotted the data as a bar plot using Seaborn.

‘Floofer’ received the highest rating on average (1.200), followed by ‘puppo’ (1.195), followed by ‘doggo’
(1.193), followed by ‘pupper’ (1.086).
