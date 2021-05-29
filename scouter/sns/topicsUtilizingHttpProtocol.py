from pygments import highlight, lexers, formatters
import subprocess
import json
import re

###############
## User Input

fileName 	= "SNS_with_http_protocol.csv"

###############

def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)

command 	= ["aws", "sns", "list-subscriptions"]
_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err 	= _subp.communicate()
out 		= json.loads(out)['Subscriptions']

writeIntoFile(fileName, stdout="Endpoint,TopicARN,Subscription ARN,Protocol\n", method='w+')
print("[~] Endpoint ~ TopicARN ~ Subscription ARN ~ Protocol")

for subscriptions in out:

	protocol 		= subscriptions['Protocol']
	topicARN 		= subscriptions['TopicArn']
	subscriptionARN	= subscriptions['SubscriptionArn']

	if protocol == "http":
		try:
			command 	= ["aws", "sns", "get-subscription-attributes", "--subscription-arn", subscriptionARN]
			_subp 		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err 	= _subp.communicate()
			out 		= json.loads(out)['Attributes']

			endpoint 	= out['Endpoint']
			print("[#] {} ~ {} ~ {} ~ {}".format(endpoint, topicARN, subscriptionARN, protocol))
			writeIntoFile(fileName, stdout="{},{},{},{}\n".format(endpoint, topicARN, subscriptionARN, protocol), method='a+')

		except KeyboardInterrupt:
			exit("[!] You killed my process :(")

		except:
			pass

print("[~] Script execution completed!\n[~] Data written in {}".format(fileName))
