#!/usr/bin/python3

from jmespath import search as queryJson
import botocore
import boto3
import json

def authorizedClientCall():
	client 		= boto3.client("ec2")
	return(client)

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def findInstanceTags(clientApiCall):
	fetchInstances 	= clientApiCall.describe_instances()
	parsingJson 	= parseJson('Reservations[*].Instances[*]', fetchInstances)
	instanceID 		= parseJson('[].InstanceId', parsingJson)
	publicDNS 		= parseJson('[].PublicDnsName', parsingJson)
	instanceTagsKey = parseJson('[].Tags[*].Key', parsingJson)
	instanceTagsVal = parseJson('[].Tags[*].Value', parsingJson)

	for ids, ips, keys, vals in zip(instanceID, publicDNS, instanceTagsKey, instanceTagsVal):
		print(f"[#] Instance ID: {ids}")
		print(f"[#] Instance IP: {ips}")
		print(f"[~] Tags: \n\n```")

		for k, v in zip(keys, vals):
			print(f"[T] {k}: {v}")

		print("```\n")

def main():
	clientCall 	= authorizedClientCall()
	findInstanceTags(clientCall)

if __name__ == '__main__':
	main()