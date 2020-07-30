import os
import json
from datetime import datetime , timedelta
import boto3

# N is the days the script will look back from the date of now.
N = 90
DELTA = datetime.now() - timedelta(days = N)
DATENOW = datetime.now()
# S3 bucket where the mails are located
DMSBUCKET = 'dms-bucket-fabio'
# Cloudtrail account and AZ
AWSUSER = 'Fabio'
REGION = 'eu-central-1'
# Mail recipients
fromaddress = 'gufoqi4v3ydw@abinemail.com'
toaddress = 'fabio.grammatico@outlook.com'
# Notification settings
status = 'success'
defaultbody = 'Dead Man Switch Job ran ' ' @ ' + str(DATENOW)
defaultsubject = 'Dead Man Switch Notification'

# You can change the temp folder to test it locally or on AWS
TEMP = '/tmp/'



def lambda_handler(event, context):
    '''
    This function will query cloudtrail for all console login in the expected region and delta from time of now
    and "N" days.
    '''
    try:
        print ('Starting lambda handler')
        client = boto3.client('cloudtrail',REGION)
        response = client.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'ConsoleLogin'
            },
        ],
        StartTime=DELTA,
        EndTime=datetime.now(),
        MaxResults=1
        )
        returnuser = response['Events'][0]['Username']
        logindate = response['Events'][0]['EventTime']
        print ('"User found ' + returnuser + ' and logindate ' + str(logindate) + '"')
        if str(returnuser) == str(AWSUSER):
            msg = defaultbody + ' with ' + status + ' status'
            mailer_func(fromaddress,toaddress,msg,status)
        else:
            deadman_switch()
    except:
        errdescr = 'Something went really,really wrong'
        print (errdescr)
        error_func(errdescr)

def error_func(errdescr):
    '''
    This function will handle the errors by setting a status and compiling a message
    '''
    try:
        status = 'failed'
        msg = defaultbody + ' with ' + status + ' status and error ' + errdescr
        mailer_func(fromaddress,toaddress,msg,status)
    except:
        print ('"The error function was in error! How did you do it????"')
        exit_func()

def deadman_switch():
    '''
    This function will trigger the dead man switch by grabbing each text files on the specified BUCKET
    and read its content.
    '''
    try:
        print ('"Dead man switch logger started"')
        s3_resource = boto3.resource('s3')
        dmsbucket = s3_resource.Bucket(DMSBUCKET)
        for s3_object in dmsbucket.objects.all():
            msg = ''
            filename = s3_object.key
            dmsbucket.download_file(s3_object.key,TEMP + filename)
            file = open(TEMP + filename, 'r')
            line = file.read()
            file.close()
            status = '\n*******'
            msg = line + status
            toaddress = filename
            os.remove(TEMP + filename)
            mailer_func(fromaddress,toaddress,msg,status)
        exit_func()
    except:
        errdescr = 'Something went really,really wrong'
        print (errdescr)
        error_func(errdescr)

def mailer_func(fromaddress,toaddress,msg,status):
    '''
    This function will produce an email
    '''
    try:
        print ('"Starting the mailer"')
        client = boto3.client('ses','eu-central-1')
        response = client.send_email(
            Source= fromaddress,
            Destination={
                'ToAddresses': [
                    toaddress,
                ]
            },
            Message={
                'Subject': {
                    'Data': defaultsubject,
                },
                'Body': {
                    'Text': {
                        'Data': msg,
                    }
                }
            }
        )
        print(response)
        print ('Mailer completed')
    except:
        errdescr = 'Something went really,really wrong'
        print (errdescr)
        exit_func()

def exit_func():
    '''
    This function is just to exit the lambda script
    '''
    return {'statusCode': 200,'body': json.dumps(status)}


# test lambda locally removing the comment below
#lambda_handler('RequestId: 371258a2-1392-478e-9125-c918b4d33182','RequestId: 371258a2-1392-478e-9125-c918b4d33182')
