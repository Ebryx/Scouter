from datetime import datetime
import subprocess
import os
import json
import re


###############
## User Input

daysToCheck	= 180
dateToday 	= datetime(2018, 12, 18) 			# Add script execution date here Y:M:D
fileName 	= "EC2_Outdated_AMIs.csv"

###############

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

print("[~] Grabbing List of AMIs (be patient)\n")
command 	= ["aws", "ec2", "describe-images", "--owners", "self", "--query", "Images[*].ImageId"]
_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= _subp.communicate()
out 		= json.loads(out)

writeIntoFile(fileName, stdout="Age (days old),EC2 Instance ID,EC2 Instance Name,EBS Volume Encryption\n", method='w+')
print("Age ~ Instance ID ~ InstanceName ~ EbsVolumeEncryption\n")

for imageId in out:
	try:
		command 			= ["aws", "ec2", "describe-images", "--image-ids", imageId]
		_subp 				= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err 			= _subp.communicate()
		out 				= json.loads(out)['Images']

		for instanceDetails in out:
			instanceName 		= instanceDetails['Name']
			ebsVolumeEncryption	= instanceDetails['BlockDeviceMappings'][0]['Ebs']['Encrypted']
			creationDate 		= instanceDetails['CreationDate']

			date 				= creationDate.split("T")[0].split("-")
			year, month, day 	= int(date[0]), int(date[1]), int(date[2])
			amiAgeInDays 		= str(dateToday - datetime(year, month, day)).split(",")[0].replace(" days", "")
			print("{:<3} ~ {} ~ {} ~ {}".format(amiAgeInDays, imageId, instanceName, str(ebsVolumeEncryption)))

			if int(amiAgeInDays) > daysToCheck: 
				writeIntoFile(fileName, stdout="{},{},{},{}\n".format(amiAgeInDays, imageId, instanceName, str(ebsVolumeEncryption)), method='a+')
	
	except KeyboardInterrupt:
		exit("[!] You killed my process :(")

	except:
		pass

print("[~] Script execution completed!\n[~] Data written in {}".format(fileName))
