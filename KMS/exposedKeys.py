from pygments import highlight, lexers, formatters
import subprocess
import json
import re


###############
## User Input

fileName 	= "KMS_exposed_keys.d"

###############

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

command 	= ["aws", "kms", "list-aliases"]
_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= _subp.communicate()
out 		= json.loads(out)['Aliases']

writeIntoFile(fileName, stdout="[~] Please find keys with JSON data [  Principal -> AWS ->  * ] yourself (since I'm not that intelligent :'( )\n\n", method='w+')
print("[~] Please find keys with JSON data [  Principal -> AWS ->  * ] from the yourself (since I'm not that intelligent :'( )\n")

for keys in out:

	ARN 			= keys['AliasArn']
	keyName 		= keys['AliasName'].replace("alias/", "")

	try: 				targetKeyID = keys['TargetKeyId']
	except KeyError: 	targetKeyID = ""

	# print(ARN, keyName, targetKeyID) # Uncomment for Debugging

	try:
		command 	= ["aws", "kms", "get-key-policy", "--key-id", targetKeyID, "--policy-name", "default", "--query", "Policy"]
		_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err 	= _subp.communicate()

		out 		= out.replace('\\"', '"').replace("\\n", "\n").replace('"{', "{").replace('}"', '}')
		out 		= json.dumps(json.loads(out), indent=4)
		
		print("[#] TargetKey ~ {}\n[#] keyName ~ {}\n[#] ARN ~ {}\n[#] Json Object ~ \n{}\n\n\n\n".format(targetKeyID, keyName, ARN, highlight(unicode(out, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())))
		writeIntoFile(fileName, stdout="[#] TargetKey ~ {}\n[#] keyName ~ {}\n[#] ARN ~ {}\n[#] Json Object ~ \n{}\n\n\n".format(targetKeyID, keyName, ARN, out), method='a+')

	except KeyboardInterrupt:
		exit("[!] You killed my process :(")

	except:
		pass

print("[~] Script execution completed!\n[~] Data written in {}".format(fileName))
