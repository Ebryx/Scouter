import subprocess
import json
import concurrent.futures

filename 	= "EC2_Unused_Keypairs.csv"

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def fetchDetailsOfKeyPair(keypair):
	command 	= ['aws', 'ec2', 'describe-instances', '--filters', 'Name=instance-state-name,Values=running', 'Name=key-name,Values="{}"'.format(keypair), '--query', 'Reservations[*].Instances[*].InstanceId']
	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err	= _subp.communicate()
	out 		= json.loads(out)

	if len(out) == 0:
		print(keypair)
		print("[!] Not attached with any instance\n")
		writeIntoFile(filename, keypair + "\n", method='a+')

	else:
		print(keypair)
		print("[#] Attached with {}\n".format(str(out)))

def main():
	writeIntoFile(filename, "Unused EC2 KeyPairs\n", method='w+')
	command 	= ["aws", "ec2", "describe-key-pairs", "--query", "KeyPairs[*].KeyName"]
	_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err	= _subp.communicate()
	keypair 	= json.loads(out)

	with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
		executor.map(fetchDetailsOfKeyPair, keypair)

if __name__ == '__main__':
	main()
