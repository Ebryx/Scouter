#!/usr/bin/python3

from jmespath import search as queryJson
import botocore
import boto3
import json

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def topicsList(clientApiCall):
	topics 		= clientApiCall.list_topics()
	topicsList 	= parseJson('Topics[*].TopicArn', topics)
	return(topicsList)

def getTopicsAttrs(topics, clientApiCall):
	topicAttrs 	= clientApiCall.get_topic_attributes(TopicArn=topics)
	policy 		= json.loads(parseJson('Attributes.Policy', topicAttrs))
	principal 	= parseJson('Statement[*]', policy)

	print(f"[#] {topics} -~> {json.dumps(principal, indent=4)}")

def main():
	clientCall 	= boto3.client("sns")
	_topics 	= topicsList(clientCall)

	print(f"[$] Topics ARN\t -~> Principal\n")

	for topics in _topics:
		getTopicsAttrs(topics, clientCall)

if __name__ == '__main__':
	main()
