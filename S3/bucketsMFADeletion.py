import concurrent.futures
import os
import subprocess
import json

PROCESSES 	= 50

print("[&] Fetching bucket details...")

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

writeIntoFile("S3_Buckets_Without_MFA_Deletion.csv", "S3 Bucket,MFA Deletion\n", method='w+')

command 	= "aws s3api list-buckets --query Buckets[*].Name"
out 		= list(json.loads(os.popen(command).read()))

print()
print(f"[#] Total buckets: {len(out)}")
print()

def getBucketVersioning(buckets):
	command 	= f"aws s3api get-bucket-versioning --bucket {buckets}"
	results 	= os.popen(command).read()

	if results == '':
		print("Bucket: " + buckets + "\n" + "ServerSideEncryptionConfiguration: " + "False" + "\n")
		writeIntoFile("S3_Buckets_Without_MFA_Deletion.csv", "{},{}\n".format(buckets, "false"), method='a+')
		return("Bucket: " + buckets + "\n" + "ServerSideEncryptionConfiguration: " + "False" + "\n")

	else:
		print("Bucket: " + buckets + "\n" + "ServerSideEncryptionConfiguration: " + "True" + "\n")
		writeIntoFile("S3_Buckets_Without_MFA_Deletion.csv", "{},{}\n".format(buckets, "true"), method='a+')
		return("Bucket: " + buckets + "\n" + "ServerSideEncryptionConfiguration: " + "True" + "\n")

with concurrent.futures.ProcessPoolExecutor(max_workers = PROCESSES) as executor:
    executor.map(getBucketVersioning, out)
