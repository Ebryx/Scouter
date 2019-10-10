import boto3
from jmespath import search as search
import fnmatch

s3 = boto3.client('s3')

def list_buckets():
	response = s3.list_buckets()
	return (response)


def main():
    """Check if a bucket exists with elasticbeanstalk as prefix"""
    
    a=list_buckets()
    
    #list containing names of the bucket
    bucket_names_list=search('Buckets[*].Name',a)
    pattern='elasticbeanstalk*'
    templates = fnmatch.filter(bucket_names_list, pattern)
    if not templates:
  		print("Couldn't find a bucket with elasticbeanstalk as perfix, so most probably there are no elasticbeanstalk configuration templates")
    else:
    	print("Please check the following buckets. Configuration templates can be found at bucket/resources/templates/app_name \n ")
    	for buckets in templates:
    		print(buckets)


if __name__ == '__main__':
    main()