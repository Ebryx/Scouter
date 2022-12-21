#!/usr/bin/python3
import os

file 	= "creds.csv"
if not(os.path.isfile(file)): exit("[>_<] Please keep IAM Credentials (i.e. creds.csv) file in the same directory of the script!!!")
dest 	= "IAM_users_with_both_console_and_cli_access.csv"

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

output 	= "Usernames,ARN,CreationDate,MfaEnabled,PasswordEnabled,AccessKeysEnabled"
results	= []

print(output)
writeIntoFile(dest, output + "\n")

with open(file, 'r') as file:
	read 	= file.read().split()

for objects in read:
	objects 	= objects.split(",")
	usernames, arn, creationDate, passwordEnabled, mfaEnabled, accesskey 	= objects[0], objects[1], objects[2].split("T")[0], objects[3], objects[7], objects[8]
	if passwordEnabled == "true" and accesskey == "true":
		output 	= usernames + "," + arn + "," + creationDate + "," + mfaEnabled + "," + passwordEnabled + "," + accesskey
		print(output)
		writeIntoFile(dest, output + "\n", "a+")
print("\n[~] Output appended in \"" + dest + "\"")
