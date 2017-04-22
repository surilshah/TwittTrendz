from kafka import KafkaProducer
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import json, geocoder

# import twitter keys and tokens
ckey = "Twitter_Consumer_Key"
csecret = "Twitter_Consumer_Secret_Key"
atoken = "Twitter_Access_Token"
asecret = "Twitter_Access_Token_Secret_Key"

producer = KafkaProducer(bootstrap_servers='localhost:9092')

class TweetStreamListener(StreamListener):
	def on_data(self, data):
		dict_data = json.loads(data)
		if 'user' in dict_data and dict_data['user']['location'] and dict_data['lang'] == 'en':
			try:
				doc = {
					'author': dict_data['user']['screen_name'],
					'date': dict_data['created_at'],
					'location': {
						'name': dict_data['user']['location'],
						'coords': {
							'lat': geocoder.google(dict_data['user']['location']).latlng[0],
							'lon': geocoder.google(dict_data['user']['location']).latlng[1]
						}
					},
					'message': dict_data['text'],
					'language': dict_data['lang']
				}
				print doc
				producer.send('tweets', json.dumps(doc))
			except Exception as e:
				print e
			return True

	def on_error(self, status):
		print status

# create instance of the tweepy tweet stream listener
listener = TweetStreamListener()
# set twitter keys/tokens
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
# create instance of the tweepy stream
stream = Stream(auth, listener)
stream.filter(track=['trump','#trump'])