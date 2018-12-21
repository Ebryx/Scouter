import subprocess
import json


########################################
## User Input

filename 	= "EC2_Unused_Keypairs.csv"

########################################


def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

writeIntoFile(filename, "Unused EC2 KeyPairs\n", method='w+')

try:
	command 	= ["aws", "ec2", "describe-key-pairs", "--query", "KeyPairs[*].KeyName"]
	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err	= _subp.communicate()
	out 		= json.loads(out)

	for keypairs in out:
		print("[~] {}".format(keypairs))
		command 	= ['aws', 'ec2', 'describe-instances', '--filters', 'Name=instance-state-name,Values=running', 'Name=key-name,Values="{}"'.format(keypairs), '--query', 'Reservations[*].Instances[*].InstanceId']
		_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err	= _subp.communicate()
		out 		= json.loads(out)
		if len(out) == 0:
			print("[!] Not attached with any instance\n")
			writeIntoFile(filename, keypairs + "\n", method='a+')

		else:
			print("[#] Attached with {}\n".format(str(out)))
except ValueError:
	pass

except KeyboardInterrupt:
	exit("[!] User Interrupted!")

except:
	pass
