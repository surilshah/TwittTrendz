from elasticsearch import Elasticsearch
from requests_aws4auth import AWS4Auth
import elasticsearch

#This python script is to create an index in elastic search with mappings specifying the type of each field

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

mappings = {
	"settings": {
		"number_of_shards": 1,
	},
	"mappings": {
	    "tweets": {
	        "properties": {
	            "author" : {
	            	"type" : "string",
	            },
	          	"date" : {
	            	"type" : "text",
	          	},
	          	"location" : {
	            	"properties" : {
	              		"coords" : {
	                		"type" : "geo_point",
	              		},
	              		"name" : {
	                		"type" : "text",
	              		}
	            	}
	        	},
	          	"message" : {
	            	"type" : "text",
	          	},
	          	"language" : {
	            	"type" : "text",
	          	},
	          	"sentiment" : {
	          		"type" : "text"
	          	}
	        }
	    }
	}
}
es.indices.create(index='tweetmap', body=mappings)