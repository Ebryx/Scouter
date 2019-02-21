# Scouter

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![python](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)

**This repository maintains some of the scripts made by Ebryx DevSecOps team**

### Requirements

- Credentials Report (from [here](https://console.aws.amazon.com/iam/home#/credential_report))
- Python (2.7.*)
- Python `pip`
- Python module `awscli`
- Python module `pygments`

### Install modules

	pip install -r requirements.txt

### Tested on

- Kali linux (subsystem)
- Ubuntu (subsystem)
 
### Download / Clone Repository

You can download the latest version by cloning this GitHub repository.

	git clone https://github.com/Ebryx/Scouter
	
## Usage
- Please run `aws configure` before running the scripts
- Each script is labelled with check name and needs to be executed manually
- Place credentials report as `creds.csv` in the same directory of script while performing IAM checks

### IAM

* [Orphan Users](https://github.com/Ebryx/Scouter/blob/master/IAM/orphanUsers.py)
* [Users with both Console && CLI access](https://github.com/Ebryx/Scouter/blob/master/IAM/consoleAndCliAccess.py)
* [Users without any IAM Group](https://github.com/Ebryx/Scouter/blob/master/IAM/usersWithoutIAMGroup.py)

### S3

* [ServerSide Encryption](https://github.com/Ebryx/Scouter/blob/master/S3/serverSideEncryption.py)

### EC2

* [Outdated AMIs](https://github.com/Ebryx/Scouter/blob/master/EC2/outdatedAMIs.py)
* [Unused KeyPairs](https://github.com/Ebryx/Scouter/blob/master/EC2/unusedKeyPairs.py)
* [Unused EIPs](https://github.com/Ebryx/Scouter/blob/master/EC2/unusedKeyPairs.py)
* [Instances without termination protection](https://github.com/Ebryx/Scouter/blob/master/EC2/instancesWithoutTerminationProtection.py)

### ElasticBeanStalk

* [ElasticBeanStalk Outdated Custom AMIs](https://github.com/Ebryx/Scouter/blob/master/ElasticBeanStalk/outdatedEBSCustomAMIs.py)

### KMS

* [Disabled KMS Keys](https://github.com/Ebryx/Scouter/blob/master/KMS/disabledKeys.py)
* [Exposed KMS Keys](https://github.com/Ebryx/Scouter/blob/master/KMS/exposedKeys.py)

### SNS

* [Topics with HTTP protcol](https://github.com/Ebryx/Scouter/blob/master/SNS/topicsUtilizingHttpProtocol.py)

### Lambda
* [Lambda Artifacts Collector](https://github.com/Ebryx/Scouter/blob/master/Lambda/lambdaArtifactsCollector.py)

### Note 
<pre><code>• Scripts will only run against resources specified by the region in `aws configure` (~/.aws/config)
• For Dependencies Issues -> <a href="https://github.com/Anon-Exploiter/SiteBroker/issues/4#issuecomment-421292969" target="_blank">Solution</a>
</code></pre>
