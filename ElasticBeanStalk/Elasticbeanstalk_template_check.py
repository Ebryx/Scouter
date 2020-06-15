#!/usr/bin/python3

import boto3
from jmespath import search as search
import fnmatch

s3 = boto3.client('s3')

def list_buckets():
	response 	= s3.list_buckets()
	return(response)

def getTemplateContents(buckets):
	"""
	Fetching contents of ElasticBeanStalk's templates 
	""" 

	appName 	= []
	tempList 	= []
	bucketsList = list_buckets()
	
	# List containing names of the bucket
	bucket_names_list	= search('Buckets[*].Name', bucketsList)
	pattern				= 'elasticbeanstalk*'
	templates 			= fnmatch.filter(bucket_names_list, pattern)

	if templates:
		for buckets in templates:
			print(f"[#] Bucket: {buckets}")
			
			objects 	= search('Contents[*].Key', s3.list_objects(Bucket=buckets))
			
			if objects:
				for _objs in objects:	
					if "resources/templates/" in _objs:
						print(_objs)
						appName.append(_objs.split("/")[2])
						tempList.append(f"{templates[0]}/{_objs}")

				for templates in tempList:
					print(f"[#] Application Name: {appName[0]}")
					print(f"[#] Template Path: {templates}")

					templateName 	= templates.replace(f'{buckets}/', '')
					_object 		= s3.get_object(Bucket=buckets, Key=templateName)
					print(f"[~] Template Contents: \n```\n{search('Body', _object).read().decode()}```\n")
	
	else:
		print("[!] Couldn't find a bucket with elasticbeanstalk as perfix, so most probably there are no elasticbeanstalk configuration templates.")

def main():
	bucketsList 	= list_buckets()
	getTemplateContents(bucketsList)

if __name__ == '__main__':
	main()
