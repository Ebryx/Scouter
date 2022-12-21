import os
import subprocess
import json

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

writeIntoFile("S3_Buckets_Without_ServerSideEncryption_Enabled.csv", "S3 Bucket,ServerSide Encryption\n", method='w+')

command 	= ["aws", "s3api", "list-buckets", "--query", "Buckets[*].Name"]
command 	= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= command.communicate()
out 		= json.loads(out)

for buckets in out:
	command 	= ["aws", "s3api", "get-bucket-encryption", "--bucket", buckets]
	command 	= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err 	= command.communicate()
	
	if out == '':
		print("Bucket: " + buckets + "\n" + "ServerSideEncryptionConfiguration: " + "False" + "\n")
		writeIntoFile("S3_Buckets_Without_ServerSideEncryption_Enabled.csv", "{},{}\n".format(buckets, "false"), method='a+')

	else:
		print("Bucket: " + buckets + "\n" + "ServerSideEncryptionConfiguration: " + "True" + "\n")
		writeIntoFile("S3_Buckets_Without_ServerSideEncryption_Enabled.csv", "{},{}\n".format(buckets, "true"), method='a+')
