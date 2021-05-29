from pygments import highlight, lexers, formatters
import subprocess
import json
import re
import concurrent.futures

fileName 	= "KMS_exposed_keys.d"

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def findExposedKeys(keys):
	ARN 			= keys['AliasArn']
	keyName 		= keys['AliasName'].replace("alias/", "")

	try: 				targetKeyID = keys['TargetKeyId']
	except KeyError: 	targetKeyID = ""

	# print(ARN, keyName, targetKeyID) # Uncomment for Debugging

	try:
		command 	= ["aws", "kms", "get-key-policy", "--key-id", targetKeyID, "--policy-name", "default", "--query", "Policy"]
		_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err 	= _subp.communicate()

		out 		= out.decode()
		out 		= out.replace('\\"', '"').replace("\\n", "\n").replace('"{', "{").replace('}"', '}')
		out 		= json.dumps(json.loads(out), indent=4)

		print("[#] TargetKey ~ {}\n[#] keyName ~ {}\n[#] ARN ~ {}\n[#] Json Object ~ \n{}\n\n\n\n".format(targetKeyID, keyName, ARN, highlight(out.encode('utf-8'), lexers.JsonLexer(), formatters.TerminalFormatter())))

		writeIntoFile(fileName, stdout="[#] TargetKey ~ {}\n[#] keyName ~ {}\n[#] ARN ~ {}\n[#] Json Object ~ \n{}\n\n\n".format(targetKeyID, keyName, ARN, out), method='a+')

	except KeyboardInterrupt:
		exit("[!] You killed my process :(")

def main():
	writeIntoFile(fileName, stdout="[~] Please find keys with JSON data [  Principal -> AWS ->  * ] yourself (since I'm not that intelligent :'( )\n\n", method='w+')
	command 	= ["aws", "kms", "list-aliases"]

	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= _subp.communicate()
	out 		= json.loads(out)['Aliases']

	print("[~] Please find keys with JSON data [  Principal -> AWS ->  * ] yourself (since I'm not that intelligent :'( )\n")

	with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
		executor.map(findExposedKeys, out)

	print("[~] Script execution completed!\n[~] Data written in {}".format(fileName))

if __name__ == '__main__':
	main()
