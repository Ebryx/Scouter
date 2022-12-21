from datetime import datetime
import subprocess
import os
import json
import re
import concurrent.futures

fileName 	= "EC2_Instances_Without_Termination_Protection.csv"

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def instancesAttributes(instanceId):
	command 	= ["aws", "ec2", "describe-instance-attribute", "--instance-id", instanceId, "--attribute", "disableApiTermination"]
	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= _subp.communicate()
	out 		= json.loads(out)

	terminationProtection 	= out['DisableApiTermination']['Value']
	print("{} ~ {}".format(instanceId, terminationProtection))
	writeIntoFile(fileName, stdout="{},{}\n".format(instanceId, terminationProtection), method='a+')

def main():
	writeIntoFile(fileName, stdout="Instance ID,Termination Protection\n", method='w+')
	print("[~] Describing EC2 Instances, may take some time depending on number of instances\n")

	command 	= ["aws", "ec2", "describe-instances", "--query", "Reservations[*].Instances[*].InstanceId[]"]
	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= _subp.communicate()
	out 		= json.loads(out)
	print("Instance ID ~ Termination Protection\n")

	with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
		executor.map(instancesAttributes, out)

	print("[~] Script execution completed!\n[~] Data written in {}".format(fileName))

if __name__ == '__main__':
	main()
