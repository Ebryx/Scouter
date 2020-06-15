#!/usr/bin/python3

from jmespath import search as queryJson
import botocore
import boto3
import json

fileName 	= "bucketsWithoutLoggingAccess.csv"

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def authorizedClientCall():
	client 		= boto3.client("cloudtrail")
	return(client)

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def listCloudtrailBuckets(clientApiCall):
	fetchStacks 	= clientApiCall.describe_trails()
	jsonData 		= parseJson('trailList[*]', fetchStacks)
	trailName 		= parseJson('[].Name', jsonData)
	trailARN 		= parseJson('[].TrailARN', jsonData)
	bucketName 		= parseJson('[].S3BucketName', jsonData)

	print("[#] Bucket Name\t ~ Access Logging\t ~ Trail Name\t ~ Trail ARN")

	for name, arn, _bucketName in zip(trailName, trailARN, bucketName):
		try:
			logging 		= boto3.client('s3').get_bucket_logging(Bucket=_bucketName)
			bucketLogging 	= parseJson('Status', logging)

			writeIntoFile(fileName, stdout="{},{},{},{}\n".format(_bucketName, str(bucketLogging), name, arn), method='a+')

			if bucketLogging == None:
				print(f"[!] {_bucketName}\t ~ {bucketLogging}\t ~ {name}\t ~ {arn}")

			else:
				print(f"[#] {_bucketName}\t ~ {bucketLogging}\t ~ {name}\t ~ {arn}")

		except botocore.exceptions.ClientError:
			print(f"[!!!] {_bucketName}\t ~ {name}\t ~ {arn} -- Access Denied")

def main():
	writeIntoFile(fileName, stdout="Bucket Name,Access Logging,Trail Name,Trail ARN\n", method='w+')
	clientCall 	= authorizedClientCall()

	listCloudtrailBuckets(clientCall)

if __name__ == '__main__':
	main()
