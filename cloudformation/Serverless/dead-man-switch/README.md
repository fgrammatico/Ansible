Dead Man Switch
===============
This Lambda will check periodically cloudtrail if your user has logged into AWS console in the last 90 days (N=90 days). 
In case of missed login the script will loop into a bucket in S3 (DMSBUCKET) for files containing the email body of your dead man switch recipients.
The files must be created as follow:

* For each file a single email recipient
* Each file must be formatted as Unicode utf-8 and named as the recipient email (myemail.com) without .txt extension
* The body must abide general python text rules so illegal characters must be escaped

Pre-requisites
----------------

* Python3 
* Pip
* AWS-cli
* Serverless cli
* Node.js 
* Valid AWS account
* A serverless-admin user with admin access with attached Role for SES,Lambda,S3,Cloudtrail
* SES Smtp with validated emails

Installation
-----------------

* Download and install Node.js https://nodejs.org/en/download/package-manager/

* Install serverless "npm install -g serverless"

* Setup serverless "serverless config credentials --provider aws --key XXX --secret YYY --profile serverless-admin"

* Edit as you please the variables in handler.py and serverless.yaml

* Clone the repository, cd into it and run "sls deploy -v"

ToDo
--------------------
Create full automation of the requirements in Ansible and cloudformation stack trigger
