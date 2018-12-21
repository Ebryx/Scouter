from datetime import datetime
import subprocess
import os
import json
import re


###############
## User Input

fileName 	= "EC2_Instances_Without_Termination_Protection.csv"

###############

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

print("[~] Describing EC2 Instances, may take some time depending on number of instances\n")
command 	= ["aws", "ec2", "describe-instances", "--query", "Reservations[*].Instances[*].InstanceId[]"]
_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= _subp.communicate()
out 		= json.loads(out)

totalInst 	= len(out)
withoutP 	= 0

writeIntoFile(fileName, stdout="Instance ID,Termination Protection\n", method='w+')
print("Instance ID ~ Termination Protection\n")

for instanceId in out:
	try:
		command 	= ["aws", "ec2", "describe-instance-attribute", "--instance-id", instanceId, "--attribute", "disableApiTermination"]
		_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err 	= _subp.communicate()
		out 		= json.loads(out)

		terminationProtection 	= out['DisableApiTermination']['Value']
		print("{} ~ {}".format(instanceId, terminationProtection))
		writeIntoFile(fileName, stdout="{},{}\n".format(instanceId, terminationProtection), method='a+')

		if terminationProtection.lower() == 'false':
			withoutP += 1

	except KeyboardInterrupt:
		exit("[!] You killed my process :(")

	except:
		pass

print("\n[#] Total Instances: {}\nInstances without Termination Protection: {}\n".format(instanceId, withoutP))
print("[~] Script execution completed!\n[~] Data written in {}".format(fileName))
