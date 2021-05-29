"""

Python2/3 based script to parse Credentials Report (creds.csv) and find orphan users based on
	-- PasswordEnabled 		-> false
	-- AccessKeysEnabled 	-> false
	-- PasswordLastUsed 	-> N/A
	-- accesskeyLastUsed 	-> N/A
	
"""

#!/usr/bin/python3
import os

#########################################
############ Editable input #############
#########################################

file 	= "creds.csv"
dest 	= "IAM_orphan_users.csv"
flag 	= {
	'passwordEnabled': 		'false',
	'accesskey': 			'false',
	'passwordLastUsed': 	  '',  		# Leave empty if you want to skip this flag / uncomment the check below
	'accesskeyLastUsed': 	  '', 		# Leave empty if you want to skip this flag / uncomment the checks below
	# 'passwordLastUsed': 	  'N/A',    # If using these flags: comment the two flags above
	# 'accesskeyLastUsed': 	  'N/A', 	# If using these flags: comment the two flags above
}

#########################################
############ Restricted Area ############
#########################################s

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

output 	= "Usernames,ARN,CreationDate,MfaEnabled,PasswordEnabled,AccessKeysEnabled,PasswordLastUsed,AccesskeyLastUsed"; print(output)
writeIntoFile(dest, output + "\n")

if not(os.path.isfile(file)): exit("[>_<] Please keep IAM Credentials (i.e. creds.csv) file in the same directory of the script!!!")

with open(file, 'r') as file:
	read 	= file.read().split()

for objects in read:
	objects 	= objects.split(",")
	usernames, arn, creationDate, passwordEnabled, passwordLastUsed, mfaEnabled, accesskey, accesskeyLastUsed 	= objects[0], objects[1], objects[2].split("T")[0], objects[3], objects[4].split("T")[0], objects[7], objects[8], objects[10].split("T")[0]
	
	if passwordEnabled == flag['passwordEnabled'] and accesskey == flag['accesskey']:
		if passwordLastUsed == flag['passwordLastUsed'] and accesskeyLastUsed == flag['accesskeyLastUsed']:
			output 	= usernames + "," + arn + "," + creationDate + "," + mfaEnabled + "," + passwordEnabled + "," + accesskey + "," + passwordLastUsed + "," + accesskeyLastUsed
			print(output) 
			writeIntoFile(dest, output + "\n", 'a+')
		
		elif flag['passwordLastUsed'] == '' and flag['accesskeyLastUsed'] == '':
			output 	= usernames + "," + arn + "," + creationDate + "," + mfaEnabled + "," + passwordEnabled + "," + accesskey + "," + passwordLastUsed + "," + accesskeyLastUsed
			print(output) 
			writeIntoFile(dest, output + "\n", 'a+')
print("\n[~] Output appended in \"" + dest + "\"")
