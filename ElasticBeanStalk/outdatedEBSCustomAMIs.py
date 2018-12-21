from datetime import datetime
import subprocess
import json

#####################################

customDate = 2018

#####################################


def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

command 	= ["aws", "elasticbeanstalk", "describe-environments"]
_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= _subp.communicate()

length    	= []
outD 		= []

objs 		= json.loads(out)
EnvName 	= objs['Environments']
print("Date | EnvironmentID | EnvironmentName | ApplicationName | SolutionStackName")
writeIntoFile("ElasticBeanStalk_Outdated_AMIs.csv", "Date,EnvironmentID,EnvironmentName,ApplicationName,SolutionStackName\n", method='w+')

for envs in EnvName:
	stack 			= envs['SolutionStackName']
	envId 			= envs['EnvironmentId']
	envName 		= envs['EnvironmentName']
	appName 		= envs['ApplicationName']
	name 			= stack.split(" ")
	name 			= name[3].split(".")
	year, month 	= name[0], name[1]
	length.append(stack)

	if int(year) != customDate:
		print(year + "-" + month + " | " + envId + " | " + envName + " | " + appName + " | " + stack)
		writeIntoFile("ElasticBeanStalk_Outdated_AMIs.csv", year + "-" + month + "," + envId + "," + envName + "," + appName + "," + stack + "\n", method='a+')
		outD.append(stack)

print("\n[#] Total no. of AMIs: {}".format(len(length)))
print("[#] Outdated AMIs: {}".format(len(outD)))
