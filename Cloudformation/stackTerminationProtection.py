#!/usr/bin/python3

from jmespath import search as queryJson
import botocore
import boto3
import json

def authorizedClientCall():
	client 		= boto3.client("cloudformation")
	return(client)

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def listCloudformationStacks(clientApiCall):
	fetchStacks 	= clientApiCall.describe_stacks()
	jsonData 		= parseJson('Stacks[*].StackName', fetchStacks)
	return(jsonData)

def getStackTerminationProtection(_stackName, clientApiCall):
	fetchData 	= clientApiCall.describe_stacks(StackName=_stackName)
	jsonData 	= parseJson('Stacks[*]', fetchData)
	termProtec 	= parseJson('[].EnableTerminationProtection', jsonData)
	StackId 	= parseJson('[].StackId', jsonData)

	for ids, stackProtection in zip(StackId, termProtec):
		if stackProtection == False:
			print(f"[!] {_stackName}\t~ {stackProtection}\t~ {ids}")

		else:
			print(f"[@] {_stackName}\t~ {stackProtection}\t~ {ids}")

def main():
	clientCall 	= authorizedClientCall()
	stacks 		= listCloudformationStacks(clientCall)

	print("[#] StackName\t\t~ TerminationProtection\t~ Stack ID")

	for _stacks in stacks:
		getStackTerminationProtection(_stacks, clientCall)

if __name__ == '__main__':
	main()