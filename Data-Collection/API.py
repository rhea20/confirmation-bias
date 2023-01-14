from flask import Flask, jsonify
from Twitter_functions import *
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

with open('Authentication/twitter_bearer_token.txt', 'r', encoding="utf8") as f:
    token = f.read()
    
with open('Authentication/database_uri.txt', 'r', encoding="utf8") as f:
    uri = f.read()

header = create_Twitter_headers(token)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

@app.route('/')
def welcome():
    return 'Welcome to my Twitter Viewer.'

@app.route('/user_tweets_and_replies/<string:userID>')
def getTweetAndReplies(userID):
    tweets = getTweetsByUserID(userID, header, 100)
    return json.dumps(tweets)

@app.route('/tweet_information/<string:tweetID>')
def getTweetInfo(tweetID):
    tweet = getSingleTweetInfo(tweetID, header)
    return json.dumps(tweet)

@app.route('/user_info/<string:username>')
def getUserInfo(username):
    info = getTwitterUserInfo(username, header)
    return json.dumps(info)

@app.route('/get_tweets_in_db')
def getTweetsInDB():
    command = 'select distinct conversation_id from comments_for_analysis'
    conn = psycopg2.connect(uri, sslmode='require')
    result = {}
    
    try:
        cur = conn.cursor()
        cur.execute(command)
        row = cur.fetchall()
        
        result['Total No. of Tweets'] = len(row)
                
        for i in row:
            text = getSingleTweetInfo(i[0], header)['data'][0]['text']
            result[i[0]] = text
        
        return json.dumps(result)
        
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    
@app.route('/get_comments_from_db/<string:tweetID>')
def getCommentsFromDB(tweetID):
    
    command = (
                '''
                select * from comments_for_analysis where conversation_id = '%s';
                ''' % tweetID
                )
    
    conn = psycopg2.connect(uri, sslmode='require')
    result = {}
    
    try:
        cur = conn.cursor()
        cur.execute(command)
        row = cur.fetchall()
        result['Total No. of Comments'] = len(row)
        result['data'] = []
                
        for i in row:
            resultDict = {}
            resultDict['id'] = i[0]
            resultDict['timestamp'] = i[1]
            resultDict['reply_to'] = i[2]
            resultDict['comment'] = i[3]
            resultDict['social_media'] = i[4]
            resultDict['head_id'] = i[5]
            resultDict['conversation_id'] = i[6]
            resultDict['user_id'] = i[7]
            result['data'].append(resultDict)
        
        return json.dumps(result)
        
    except (Exception, psycopg2.DatabaseError) as error:
        return error
        
@app.route('/get_media_bias/<string:news_provider>')        
def getMediaBias(news_provider):
    string_input = re.sub(' ', '-', news_provider)

    URL = f"https://mediabiasfactcheck.com/{string_input}/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find_all('title')[0]

    paras = soup.find_all('p')[0:3]
    rating = str(paras[1])
    rating_output = BeautifulSoup(rating).get_text().split('\n')
    
    result = {'About': BeautifulSoup(str(title)).get_text()}
    for i in rating_output:
        res = i.split(':')
        result[res[0]] = res[1]
        
    return json.dumps(result)