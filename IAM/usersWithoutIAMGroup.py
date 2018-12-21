import subprocess
import json
import os

filename 	= 'IAM_users_without_any_groups.csv'

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

output 		= "Usernames,ARN,CreationDate,GroupCount"; writeIntoFile(filename, output + "\n", method='w+')

command 	= ['aws', 'iam', 'list-users']
command 	= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= command.communicate()
out 		= json.loads(out)


users 		= out['Users']
for _users in users:
	username 	= _users['UserName']
	creationD 	= _users['CreateDate'].split("T")[0]
	arn 		= _users['Arn']

	command 	= ['aws', 'iam', 'list-groups-for-user', '--user-name', username]
	command 	= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= command.communicate()
	out 		= json.loads(out)
	out 		= out['Groups']
	print(username)
	print("Group Count: " + str(len(out)) + "\n")

	if len(out) == 0:
		output 	= username + "," + arn + "," + creationD + "," + str(len(out))
		print(output)
		writeIntoFile(filename, output + "\n", method='a+')
