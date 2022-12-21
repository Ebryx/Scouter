from botocore.exceptions import ClientError

import concurrent.futures
import boto3
import json

FILENAME 	= "S3_Buckets_Without_MFA_Deletion.csv"
PROCESSES 	= 50

clientCall	= boto3.client('s3')

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def getBucketVersioning(buckets):
	try:
		versioning 	= clientCall.get_bucket_versioning(Bucket=buckets)
		status 		= json.loads(json.dumps(versioning, default=str))

		if "Status" in status:
			print(f'{buckets} | True')
			writeIntoFile(FILENAME, f"{buckets},True\n", method='a+')

		else:
			print(f'{buckets} | False')
			writeIntoFile(FILENAME, f"{buckets},False\n", method='a+')

	except:
		print(f'{buckets} | False')
		writeIntoFile(FILENAME, f"{buckets},False\n", method='a+')

def main():
	print("[&] Fetching bucket details...")
	writeIntoFile(FILENAME, "S3 Bucket,MFA Deletion\n", method='w+')

	s3buckets 	= []

	response 	= clientCall.list_buckets()['Buckets']

	for buckets in response:
		s3buckets.append(buckets['Name'])

	print()
	print(f"[#] Total buckets: {len(s3buckets)}")
	print()

	# for buckets in s3buckets:
	# 	getBucketVersioning(buckets)

	with concurrent.futures.ProcessPoolExecutor(max_workers = PROCESSES) as executor:
		executor.map(getBucketVersioning, s3buckets)

if __name__ == '__main__':
	main()