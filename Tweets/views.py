from django.shortcuts import render
from elasticsearch import Elasticsearch
from requests_aws4auth import AWS4Auth
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json, geocoder, elasticsearch

# Create your views here.
def es_conn():
    # create instance of elasticsearch
    host = 'ElasticSearch_Host' #Creata a domain on ElasticSearch Service and add the endpoint here
    awsauth = AWS4Auth('AWS_Access_Key', 'AWS_Access_Secret_Key', 'AWS_Region', 'es')
    es = elasticsearch.Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=elasticsearch.connection.RequestsHttpConnection
    )
    return es

def index(request):
    return render(request,"home.html",{})

@csrf_protect
def home(request):
    query = str(request.POST.get('myword'))
    es = es_conn()
    res = es.search(size=5000, index="tweetmap", doc_type="tweets", body={
        "query":{
            "match": {
                "message": query
            }
        }
    })
    return render(request,"index.html",{'my_data':json.dumps(res), 'query':query})

@csrf_exempt
def notifications(request):
    body = json.loads(request.body.decode("utf-8"))
    print(type(body))
    hdr = body['Type']
    if hdr == 'SubscriptionConfirmation':
        url = body['SubscribeURL']
        print("Subscription Confirmation - Visiting URL : " + url)
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        print(r.status)
    if hdr == 'Notification':
        print("SNS Notification")
        tweet = json.loads(body['Message'])
        es = es_conn();
        es.index(index='tweetmap', doc_type='tweets', body=tweet)
        if not tweetQueue.full() and flag == False:
            tweetQueue.put(tweet)
            print("Tweet in queue")
    return HttpResponse(status=200)