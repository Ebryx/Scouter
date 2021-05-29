#!/usr/bin/python3

from jmespath import search as queryJson
import botocore
import boto3
import json

def authorizedClientCall():
	client 		= boto3.client("redshift")
	return(client)

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def publicRedshiftInstances(clientApiCall):
	fetchClusters 	= clientApiCall.describe_clusters()
	jsonData 		= parseJson('Clusters[*]', fetchClusters)
	clusterName 	= parseJson('[].ClusterIdentifier', jsonData)
	redSIsPublic 	= parseJson('[].PubliclyAccessible', jsonData)

	print("[$] Cluster Name\t ~ Publicy Publicly Accessible?")

	for dbs, isPublic in zip(clusterName, redSIsPublic):
		if isPublic == 'true':
			print(f"[#] {dbs}\t ~ {isPublic}")

		else:
			print(f"[!] {dbs}\t ~ {isPublic}")

def main():
	clientCall 	= authorizedClientCall()
	publicRedshiftInstances(clientCall)

if __name__ == '__main__':
	main()