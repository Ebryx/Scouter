#!/usr/bin/python3

"""
Dependencies:
	- Aria2 (sudo apt install aria2c)
	- Python3 (sudo apt install python3)
	- Python3-Pip (sudo apt install python3-pip)
	- ZipGrep (sudo apt install zipgrep)
	- Zip & Unzip (sudo apt install zip unzip)
	- AWSCLI (pip install awscli)
	- Access keys to be situated in ~/.aws/credentials

- Installing all at once...
>>> sudo apt install aria2 python3 python3-pip zip unzip && pip install awscli

"""

import subprocess
import json
import sys
import os

def createDirs(path):
	if not os.path.exists(f"{path}/data/"):
		print(f"[~] Creating Directory: {path}/data/")
		os.makedirs(f"{path}/data/")

		print(f"[#] Creating Directory /downloads/ in parent directory: {path}/data/")
		os.makedirs(f"{path}/data/downloads/")

def logData(filename, mode, stdout):
	with open(filename, mode) as handler: handler.write(stdout)

def makeListFunctionCall():
	command 	= ['aws', 'lambda', 'list-functions']
	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= _subp.communicate()
	return(out)

def listLambdaFunction(data):
	out 			= json.loads(data)['Functions']
	functionsList 	= []
	print(f"\n[~] Total number of lambda functions: {len(out)}")
	
	for count in range(len(out)):
		print( f"[#] {out[count]['FunctionName']}" )
		functionsList.append(out[count]['FunctionName'])
	
	return(json.dumps(functionsList))

def returnLambdaFunctionAddress(functionName):
	command 	= ['aws', 'lambda', 'get-function', '--function-name', functionName]
	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= _subp.communicate()
	out 		= json.loads(out)
	print(f"[#] Address for Lambda function `{functionName}` >> \"{out['Code']['Location']}\"\n")
	return(out['Code']['Location'])

def downloadLambdaFunction(path, functionName, functionAddr):
	functionName 	= f"./data/downloads/{functionName}"
	command 		= ['aria2c', '-s', '10', '-j', '10', '-x', '16', functionAddr, '-o', functionName]
	_subp 			= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 		= _subp.communicate()
	print(out.decode())

def getEnvVariables(apiCall):
	logData('functionEnvs.csv', 'w+', 'Function Name,Data\n')
	apiCall 	= json.loads(apiCall)['Functions']

	for count in range(len(apiCall)):
		functionName 	= apiCall[count]['FunctionName']
		
		if "Environment" in apiCall[count]:
			if "Variables" in apiCall[count]['Environment']:
				functionEnvs 	= apiCall[count]['Environment']['Variables']
				logData('functionEnvs.csv', 'a+', f"{functionName},{functionEnvs}\n"); print(functionName, functionEnvs)

def parseFunctions(regexPatterns,  functionsPath):
	logData('functionsParsedData.csv', 'w+', 'Function Name,Parsed Data\n')

	for lambdaFunctions in os.listdir(functionsPath):
		functions 	= f"{functionsPath}/{lambdaFunctions}"
		print(f"[#] Analyzing {lambdaFunctions}")

		for patterns in regexPatterns:
			command 	= ["zipgrep", "-HE", patterns, functions]
			_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err 	= _subp.communicate()
			out 		= out.decode().strip()

			if out != "":
				print(out)
				logData('functionsParsedData.csv', 'a+', f'{lambdaFunctions},{out}\n')

	print()

def main():
	regexPatterns = [
		'AKIA',             # For finding access keys
		'Slacker',
		'USERNAME\|USER',
		'PASSWORD\|PASS',
	    'xox'               # Slack User's private token
		#'[[:xdigit:]][[:xdigit:]]:[[:xdigit:]][[:xdigit:]]:[[:xdigit:]][[:xdigit:]]:[[:xdigit:]][[:xdigit:]]'
	]

	print("[$] Alright World, Its time to take you on!")

	path 		= os.getcwd()
	createDirs(path)

	apiCall 			= makeListFunctionCall()
	lambdaFunctions 	= listLambdaFunction(apiCall); print()
	getEnvVariables(apiCall); print()
	
	for functions in json.loads(lambdaFunctions):
		functionName 	= f"./data/downloads/{functions}"
		
		if not os.path.exists(functionName):
			functionAddr 	= returnLambdaFunctionAddress(functions)
			downloadLambdaFunction(path, functions, functionAddr)
	
	parseFunctions(regexPatterns, f"./data/downloads/")

if __name__ == '__main__':
	main()

