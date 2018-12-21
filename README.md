## Scouter

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![python](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)

**This repository maintains scripts for performing AWS SA (Security Assessment) checks which aren't performed by Scout2**

### Requirements

- Credentials Report (from [here](https://console.aws.amazon.com/iam/home#/credential_report))
- Python (2.7.*)
- Python `pip`
- Python module `awscli`
- Python module `pygments`

### Install modules

	pip install -r requirements.txt

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
