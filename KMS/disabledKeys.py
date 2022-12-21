import subprocess
import json
import re
import concurrent.futures

fileName 	= "KMS_disabled_keys.csv"

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def findKeyStatus(keys):
	command 	= ["aws", "kms", "describe-key", "--key-id", keys]
	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= _subp.communicate()
	params 		= json.loads(out)['KeyMetadata']

	keyId 		= params['KeyId']
	description	= params['Description']
	arn 		= params['Arn']
	state 		= params['KeyState']

	print("[~] {} ~ {} ~ {} ~ {}".format(keyId, description, arn, state))
	writeIntoFile(fileName, stdout="{},{},{},{}\n".format(keyId, description, arn, state), method='a+')

def main():
	writeIntoFile(fileName, stdout="KMS Key,Description,ARN,State\n", method='w+')
	command 	= ["aws", "kms", "list-keys", "--query", "Keys[*].KeyId"]

	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= _subp.communicate()
	out 		= json.loads(out)

	print("[#] KMS Key ~ ARN ~ Description ~ State \n")

	with concurrent.futures.ProcessPoolExecutor(max_workers=30) as executor:
		executor.map(findKeyStatus, out)

	print("[~] Script execution completed!\n[~] Data written in {}".format(fileName))

if __name__ == '__main__':
	main()
