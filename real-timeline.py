#-*- coding: utf-8 -*-

import sys, json, time

try:
	import tweepy
except ImportError:
	print "Unfortunately, tweepy package was not installed on your system. Please try to execute 'pip install tweepy' beforehand."

#stores required keys in global variables
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

#OAuthHandler handshake
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# class implementation for Twitter Stream API
class streamListener(tweepy.StreamListener):
    def __init__(self):
        self.counter = 0
        self.output  = open(time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.delout  = open('delete.txt', 'a')

    def on_data(self, data):

        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return false

    def on_status(self, status):
        self.output.write(status + "\n")
        self.counter += 1

        if self.counter >= 20000:
            self.output.close()
            self.output = open('../streaming_data/' + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0

        return

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 

def main():
    listen = streamListener()
    stream = tweepy.Stream(auth, listen)

    sys.argv.pop(0)
    print (sys.argv)
    track = str(sys.argv)

    print "Streaming started..."

    try: 
        stream.filter(track = track)
    except:
        print "error!"
        stream.disconnect()

if __name__ == '__main__':
	main()
