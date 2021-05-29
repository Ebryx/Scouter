from botocore.exceptions import ClientError

import concurrent.futures
import boto3
import json

FILENAME 	= "S3_Buckets_Without_Encryption.csv"
PROCESSES 	= 50

clientCall	= boto3.client('s3')

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

def getBucketEncryption(buckets):
	try:
		encryption 	= clientCall.get_bucket_encryption(Bucket=buckets)
		print(f'{buckets} | True')
		writeIntoFile(FILENAME, f"{buckets},True\n", method='a+')

	except :
		print(f'{buckets} | False')
		writeIntoFile(FILENAME, f"{buckets},False\n", method='a+')

def main():
	print("[&] Fetching bucket details...")
	writeIntoFile(FILENAME, "S3 Bucket,Encryption\n", method='w+')

	s3buckets 	= []

	response 	= clientCall.list_buckets()['Buckets']

	for buckets in response:
		s3buckets.append(buckets['Name'])

	print()
	print(f"[#] Total buckets: {len(s3buckets)}")
	print()

	# for buckets in s3buckets:
	# 	getBucketEncryption(buckets, s3)

	with concurrent.futures.ProcessPoolExecutor(max_workers = PROCESSES) as executor:
		executor.map(getBucketEncryption, s3buckets)

if __name__ == '__main__':
	main()