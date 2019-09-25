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

def checkDetailedMonitoring(clientApiCall):
	fetchInstances 	= clientApiCall.describe_instances()
	parsingJson 	= parseJson('Reservations[*].Instances[*]', fetchInstances)
	instanceID 		= parseJson('[].InstanceId', parsingJson)
	publicDNS 		= parseJson('[].PublicDnsName', parsingJson)
	monitoringState = parseJson('[].Monitoring.State', parsingJson)
	print("[#] Instance ID ~ Monitoring Status ~ External IP")

	for ids, ips, status in zip(instanceID, publicDNS, monitoringState):
		if status == "disabled":
			print(f"[!] {ids} ~ {status} ~  {ips}".format(ids, status, ips))

		else:
			print(f"[#] {ids} ~ {status} ~  {ips}".format(ids, status, ips))

def main():
	clientCall 	= authorizedClientCall()
	checkDetailedMonitoring(clientCall)

if __name__ == '__main__':
	main()