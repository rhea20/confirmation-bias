# Data-Collection
Repository to collect and pre-process the social media data collected from Twitter and Reddit APIs, and the [PHEME dataset](https://figshare.com/articles/dataset/PHEME_dataset_for_Rumour_Detection_and_Veracity_Classification/6392078/1).

# Running the APIs

1. Clone copy of repository.
2. Run the following commands.

`set FLASK_APP=API.py`

`flask run`

# About the API Endpoints

`/user_tweets_and_replies/<userID>`

Obtain the tweets and replies of a specific user based on the user identifier

`/tweet_info/<tweetID>`

Obtain the information relating to a specific tweet based on the tweet identifier.

`/user_info/<username>`

Obtain information relating to specific account based on the user's username.

`/liked_posts/<userID>`

View the posts liked by a specific user based on the user identifier.

`/get_tweets_in_db`

Obtain all the tweets posted by news provider that are currently saved in the PostgreSQL database.

`/get_comments_from_db/<tweetID`

Obtain all the comments of the specifc tweet that are saved in the PostgreSQL database based on the tweet identifier.

`/get_media_bias/<news_provider>`

Obtain the media bias scores from the Media Bias/ Fact Check website based on the name of the news provider.
