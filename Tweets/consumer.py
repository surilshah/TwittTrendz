from kafka import KafkaConsumer
from textblob import TextBlob
import time, json, boto3

consumer = KafkaConsumer('tweets', bootstrap_servers='localhost:9092')
sns = boto3.resource('sns')
topic = sns.Topic('SNS_Topic_ARN') #Enter your SNS Topic ARN

for msg in consumer:
	doc = json.loads(msg.value)
	sent = TextBlob(doc['message'])
	a = sent.sentiment.polarity
	if a > 0.25:
		doc['sentiment'] = 'positive'
	elif a < -0.25:
		doc['sentiment'] = 'negative'
	else:
		doc['sentiment'] = 'neutral'
	print doc
	time.sleep(1)
	response = topic.publish(Message=json.dumps(doc))