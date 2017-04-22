from multiprocessing.dummy import Pool as ThreadPool
from kafka import KafkaConsumer
from textblob import TextBlob
import time, json, boto3

sns = boto3.resource('sns')
topic = sns.Topic('SNS_Topic_ARN') #Enter your SNS Topic ARN

def getData(n):
	consumer = KafkaConsumer('tweets', bootstrap_servers='localhost:9092')
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
	return doc

def calculateParallel(numbers, threads):
    # configuring the worker pool
    pool = ThreadPool(threads)
    results = pool.map(getData,numbers)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6]
    for n in range(50):
        tweet_text = calculateParallel(numbers, 10)
        print(n)