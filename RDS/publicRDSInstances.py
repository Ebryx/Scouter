#!/usr/bin/python3

from jmespath import search as queryJson
import botocore
import boto3
import json

def authorizedClientCall():
	client 		= boto3.client("rds")
	return(client)

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def publicRdsInstances(clientApiCall):
	fetchInstances 	= clientApiCall.describe_db_instances()
	jsonData 		= parseJson('DBInstances[*]', fetchInstances)
	dbInstances 	= parseJson('[].DBInstanceIdentifier', jsonData)
	rdsIsPublic 	= parseJson('[].PubliclyAccessible', jsonData)
	rdsSecGroup 	= parseJson('[].VpcSecurityGroups[*].VpcSecurityGroupId[]', jsonData)

	for dbs, isPublic, secGroup in zip(dbInstances, rdsIsPublic, rdsSecGroup):
		print(f"[#] DB Instance Name: {dbs}")
		print(f"[#] Is Db Instance Public?: {isPublic}")
		print(f"[#] Security Group ID: {secGroup}")
		print("\n[~] Security Group JSON Policy:\n```")

		describeSG 	= boto3.client("ec2").describe_security_groups(GroupIds=[secGroup])
		print(f"{json.dumps(describeSG['SecurityGroups'][0], indent=4)}\n```")

def main():
	clientCall 	= authorizedClientCall()
	publicRdsInstances(clientCall)

if __name__ == '__main__':
	main()