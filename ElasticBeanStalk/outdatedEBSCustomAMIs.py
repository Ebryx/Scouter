from datetime import datetime
import subprocess
import json

fileName 		= "ElasticBeanStalk_Outdated_AMIs.csv"
daysToCheck		= 180
dateToday 		= datetime(2020, 6, 12) 			# Add script execution date here Y:M:D

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

command 	= ["aws", "elasticbeanstalk", "describe-environments"]
_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= _subp.communicate()

objs 		= json.loads(out)
EnvName 	= objs['Environments']

print("Date | EnvironmentID | EnvironmentName | ApplicationName | SolutionStackName")
writeIntoFile("ElasticBeanStalk_Outdated_AMIs.csv", "Date,EnvironmentID,EnvironmentName,ApplicationName,SolutionStackName\n", method='w+')

for envs in EnvName:
	stack 				= envs['SolutionStackName']
	updationDate 		= envs['DateUpdated']
	envId 				= envs['EnvironmentId']
	envName 			= envs['EnvironmentName']
	appName 			= envs['ApplicationName']

	date 				= updationDate.split("T")[0].split("-")
	year, month, day 	= int(date[0]), int(date[1]), int(date[2])
	amiAgeInDays 		= str(dateToday - datetime(year, month, day)).split(",")[0].replace(" days", "")

	print("{:<3} | {} | {} | {} | {}".format(amiAgeInDays, envId, envName, appName, stack))

	try:
		if int(amiAgeInDays) > daysToCheck:
			writeIntoFile(fileName, stdout="{},{},{},{}\n".format(amiAgeInDays, envId, envName, appName, stack), method='a+')

	except ValueError:
		pass
