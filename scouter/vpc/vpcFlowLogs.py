#!/usr/bin/python3

from jmespath import search as queryJson
import botocore
import boto3
import json

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def vpcFlowLogs(clientApiCall):
	fetchVPCS 	= clientApiCall.describe_vpcs()
	vpcsID 		= parseJson('Vpcs[*].VpcId', fetchVPCS)

	print("[$] VPC ID\t~ LogDestination\t~ FlowLogId")
	
	for ids in vpcsID:
		checkFlowLogs 	= clientApiCall.describe_flow_logs(Filters=[{'Name': 'resource-id', 'Values': [ids]}])
		LogDestination 	= parseJson('FlowLogs[*].LogDestination', checkFlowLogs)
		flowLogId 		= parseJson('FlowLogs[*].FlowLogId', checkFlowLogs)

		if len(checkFlowLogs['FlowLogs']) != 0:
			print(f"[#] {ids}\t~ {LogDestination}\t~ {flowLogId}")

		else:
			print(f"[!] {ids}\t~ Not Enabled\t~ Not Enabled")

def main():
	clientCall 	= boto3.client("ec2")
	vpcFlowLogs(clientCall)

if __name__ == '__main__':
	main()