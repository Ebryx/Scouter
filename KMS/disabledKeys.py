import subprocess
import json
import re


###############
## User Input

fileName 	= "KMS_disabled_keys.csv"

###############

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

command 	= ["aws", "kms", "list-keys", "--query", "Keys[*].KeyId"]
_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= _subp.communicate()
out 		= json.loads(out)

writeIntoFile(fileName, stdout="KMS Key,Description,ARN,State\n", method='w+')
print("[#] KMS Key ~ ARN ~ Description ~ State \n")

for keys in out:
	try:
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

	except KeyboardInterrupt:
		exit("[!] You killed my process :(")

	except:
		pass

print("[~] Script execution completed!\n[~] Data written in {}".format(fileName))
