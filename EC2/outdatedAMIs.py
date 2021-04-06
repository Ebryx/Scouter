#!/usr/bin/python3

import concurrent.futures

import datetime
import json
import boto3
import subprocess

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def ec2Client(service):
	client 	= boto3.client(service)
	return(client)

def describeAMIsDuration(ec2Client, dateToday, fileName, daysToCheck):
	descImg 	= ec2Client.describe_images(Owners = ['self'])
	images 		= json.loads(json.dumps(descImg))['Images']

	for instanceDetails in images:
		imageId 		= instanceDetails['ImageId']
		instanceName 		= instanceDetails['Name']
		ebsVolumeEncryption	= instanceDetails['BlockDeviceMappings'][0]['Ebs']['Encrypted']
		creationDate 		= instanceDetails['CreationDate']

		date 				= creationDate.split("T")[0].split("-")
		year, month, day 	= int(date[0]), int(date[1]), int(date[2])

		amiAgeInDays 		= str(dateToday - datetime.datetime(year, month, day)).split(" ")[0]

		if ":" in amiAgeInDays:
			amiAgeInDays 	= 0

		print("{:<3} ~ {} ~ {} ~ {}".format(amiAgeInDays, imageId, instanceName, str(ebsVolumeEncryption)))

		if int(amiAgeInDays) > daysToCheck: 
			writeIntoFile(fileName, stdout="{},{},{},{}\n".format(amiAgeInDays, imageId, instanceName, str(ebsVolumeEncryption)), method='a+')

def main():
	daysToCheck	= 180
	service 	= 'ec2'
	dateToday 	= datetime.datetime.today()
	fileName 	= "EC2_Outdated_AMIs.csv"

	print(f"[~] Grabbing List of AMIs (be patient) -- Checking with respect to '{daysToCheck} days'\n")
	writeIntoFile(fileName, stdout="Age (days old),EC2 Instance ID,EC2 Instance Name,EBS Volume Encryption\n", method='w+')

	client 		= ec2Client(service)
	images 		= describeAMIsDuration(client, dateToday, fileName, daysToCheck)

	print("\n[~] Script execution completed!\n[~] Data written in {}".format(fileName))

if __name__ == '__main__':
	main()
