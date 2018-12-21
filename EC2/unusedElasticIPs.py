from datetime import datetime
import subprocess
import os
import json
import re


###############
## User Input

fileName 	= "EC2_Unused_Elastic_IPs.csv"

###############

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

print("[~] Grabbing List of Unused Elastic IPs (be patient)\n")

command 	= ["aws", "ec2", "describe-addresses"]
_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= _subp.communicate()
out 		= json.loads(out)['Addresses']

writeIntoFile(fileName, stdout="Public IP,Allocation ID\n", method='w+')
print("Public IP ~ Allocation ID\n")

for eip in out:
	try:
		networkIntId 	= eip['NetworkInterfaceOwnerId']
	
	except KeyError:
		publicIP 		= eip['PublicIp']
		allocationId 	= eip['AllocationId']

		print("{} ~ {}".format(publicIP, allocationId))
		writeIntoFile(fileName, stdout="{},{}\n".format(publicIP, allocationId), method='a+')	

	except KeyboardInterrupt:
		exit("[!] You killed my process :(")

	except:
		pass

print("\n[~] Script execution completed!\n[~] Data written in {}".format(fileName))
