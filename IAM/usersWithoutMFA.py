#!/usr/bin/python3
import os

file 	= "creds.csv"
dest 	= "IAM-usersWithoutMFA.csv"
if not(os.path.isfile(file)): exit("[>_<] Please keep IAM Credentials (i.e. creds.csv) file in the same directory of the script!!!")

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

output 	= "Usernames,ARN,CreationDate,MfaEnabled"; print(output)
writeIntoFile(dest, output + "\n", 'w+')

with open(file, 'r') as file: read 	= file.read().split()

for objects in read:
	objects 	= objects.split(",")
	usernames, arn, creationDate, mfaEnabled 	= objects[0], objects[1], objects[2].split("T")[0], objects[7]
	
	if mfaEnabled == 'false':
		output 	= usernames + "," + arn + "," + creationDate + "," + mfaEnabled
		print(output) 
		writeIntoFile(dest, output + "\n", 'a+')
		
print("\n[~] Output appended in \"" + dest + "\"")