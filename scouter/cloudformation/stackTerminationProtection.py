#!/usr/bin/python3

from jmespath import search as queryJson
import botocore
import boto3
import json
import concurrent.futures

fileName 	= "Cloudformation_Stacks_without_TerminationProtection.csv"

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def authorizedClientCall():
	client 		= boto3.client("cloudformation")
	return(client)

clientCall 	= authorizedClientCall()

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def listCloudformationStacks():
	fetchStacks 	= clientCall.describe_stacks()
	jsonData 		= parseJson('Stacks[*].StackName', fetchStacks)
	return(jsonData)

def getStackTerminationProtection(_stackName):
	fetchData 	= clientCall.describe_stacks(StackName=_stackName)
	jsonData 	= parseJson('Stacks[*]', fetchData)

	termProtec 	= parseJson('[].EnableTerminationProtection', jsonData)
	StackId 	= parseJson('[].StackId', jsonData)

	for ids, stackProtection in zip(StackId, termProtec):
		writeIntoFile(fileName, stdout="{},{},{}\n".format(_stackName, stackProtection, ids), method='a+')

		if stackProtection == False:
			print(f"[!] {_stackName}\t~ {stackProtection}\t~ {ids}")

		else:
			print(f"[@] {_stackName}\t~ {stackProtection}\t~ {ids}")

def main():
	writeIntoFile(fileName, stdout="StackName,Termination Protection,Stack ID\n", method='w+')
	stacks 		= listCloudformationStacks()

	print("[#] StackName\t\t~ TerminationProtection\t~ Stack ID")

	with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
		executor.map(getStackTerminationProtection, stacks)

if __name__ == '__main__':
	main()
