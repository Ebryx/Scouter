import subprocess
import json
import os
import concurrent.futures

filename 	= 'IAM_users_without_any_groups.csv'

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)
 
def getUsersGroups(username):
	user 		= username['UserName']
	creationD 	= username['CreateDate'].split("T")[0]
	arn 		= username['Arn']

	command 	= ['aws', 'iam', 'list-groups-for-user', '--user-name', user]
	command 	= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= command.communicate()
	out 		= json.loads(out)
	out 		= out['Groups']

	print("[#] " + user)
	print("```")
	print("Group Count: " + str(len(out)))

	if len(out) == 0:
		output 	= user + "," + arn + "," + creationD + "," + str(len(out))
		writeIntoFile(filename, output + "\n", method='a+')
		print(output)

	print("```\n")

def main():
	output 		= "Usernames,ARN,CreationDate,GroupCount"; writeIntoFile(filename, output + "\n", method='w+')
	command 	= ['aws', 'iam', 'list-users']
	command 	= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= command.communicate()
	out 		= json.loads(out)
	users 		= out['Users']

	with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
		executor.map(getUsersGroups, users)

if __name__ == '__main__':
	main()
