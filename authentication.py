import tweepy
import sys

try:
	import tweepy 
except ImportError:
	print "Unfortunately, tweepy package was not installed on your system. Please try to execute 'pip install tweepy' beforehand."

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

try:
	file = open("credentials.txt","r")
	credentials = file.read()
	consumer_key, consumer_secret, access_token, access_token_secret = credentials.split(",")
except IOError:
	file = open("credentials.txt","w")
	consumer_key = raw_input("Please insert your consumer_key: ")
	consumer_secret = raw_input("Please insert your consumer_secret: ")
	access_token = raw_input("Please insert your access_token: ")
	access_token_secret = raw_input("Please insert your access_token_secret: ")
	file.write(consumer_key + "," + consumer_secret + "," + access_token + "," + access_token_secret)
file.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
	print tweet.text