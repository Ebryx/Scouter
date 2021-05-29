#!/usr/bin/python3

from jmespath import search as queryJson
import botocore
import boto3
import json
import concurrent.futures

fileName 	= "Cloudfront-distributions_without_logging_enabled.csv"

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def authorizedClientCall():
	client 		= boto3.client("cloudfront")
	return(client)

clientCall 	= authorizedClientCall()

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def returnDistributionIDs():
	fetchDists	 	= clientCall.list_distributions()
	jsonData 		= parseJson('DistributionList.Items[*].Id', fetchDists)
	print(f"[#] Total Dists: {len(jsonData)}")
	return(jsonData)

def getCloudfrontDistLoggingStatus(dists):
	fetchedData 	= clientCall.get_distribution(Id=dists)
	arn 			= parseJson('Distribution.ARN', fetchedData)
	modifiedDate	= str(parseJson('Distribution.LastModifiedTime', fetchedData)).split(" ")[0]
	distSubd 		= parseJson('Distribution.DomainName', fetchedData)
	loggingStatus	= parseJson('Distribution.DistributionConfig.Logging.Enabled', fetchedData)

	try: cname 		= parseJson('Distribution.AliasICPRecordals[*].CNAME', fetchedData)[0]
	except TypeError: cname = "None"

	print(dists, arn, modifiedDate, distSubd, cname, loggingStatus)

	if loggingStatus == False:
		writeIntoFile(fileName, stdout=f"{dists},{arn},{modifiedDate},{distSubd},{cname},{loggingStatus}\n", method='a+')

def main():
	writeIntoFile(fileName, stdout="Distribution ID,ARN,Modified Date,Cloudfront URL,CNAME,Logging Status\n", method='w+')
	dists 		= returnDistributionIDs()

	# for _dists in dists:
	# 	getCloudfrontDistLoggingStatus(_dists)

	print("[#] Distribution ID\t\t~ ARN\t~ Modified Date\t~ Cloudfront URL\t~ CNAME\t~ Logging Status")

	with concurrent.futures.ProcessPoolExecutor(max_workers = 10) as executor:
		executor.map(getCloudfrontDistLoggingStatus, dists)

if __name__ == '__main__':
	main()
