import os
import json
import logging
import smtplib
from datetime import datetime , timedelta
import boto3
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
#date
N = 90
DELTA = datetime.now() - timedelta(days = N)
DATENOW = datetime.now()
#ses credentials
SESUSR = 'key'
SESPASS = 'secret'
#s3 credentials
DMSBUCKET = 'bucket'
#cloudtrail
AWSUSER = 'your username'
REGION = 'your region'
#smtp
SMPTPORT = 587
smtpserver = 'email-smtp.' + REGION + '.amazonaws.com'
fromaddress = 'enteryourmail@mail.com'
toaddress = 'enteryourmail@mail.com'
status = 'success'
body ='''\
Subject: Dead Man Switch report

This message is sent to inform you that the Dead Man Switch ran @ ''' + str(DATENOW)
# You can change the temp folder to test it locally or on AWS
TEMP = '/tmp/'



def lambda_handler(event, context):
    '''
    This function will query cloudtrail for all console login in the expected region and delta from time of now
    and "N" days.
    '''
    try:
        logger.info('Starting lambda handler')
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
        logger.info('"User found ' + returnuser + ' and logindate ' + str(logindate) + '"')
        if str(returnuser) == str(AWSUSER):
            msg = body + ' with a ' + status + ' status'
            mailer_func(fromaddress,toaddress,msg,status)
        else:
            deadman_switch()
    except Exception as error:
        errdescr = type(error).__name__ + '\n' + traceback.format_exc()
        logger.info(errdescr)
        error_func(errdescr)

def error_func(errdescr):
    '''
    This function will handle the errors by setting a status and compiling a message
    '''
    try:
        status = 'failed'
        msg = body + ' with ' + status + ' status and error ' + errdescr
        mailer_func(fromaddress,toaddress,msg,status)
    except:
        logger.info('"The error function was in error! How did you do it????"')
        exit_func()

def deadman_switch():
    '''
    This function will trigger the dead man switch by grabbing each text files on the specified BUCKET
    and read its content.
    '''
    try:
        logger.info('"Dead man switch logger started"')
        s3_resource = boto3.resource('s3')
        dmsbucket = s3_resource.Bucket(DMSBUCKET)
        for s3_object in dmsbucket.objects.all():
            msg = ''
            filename = s3_object.key
            dmsbucket.download_file(s3_object.key,TEMP + filename)
            file = open(TEMP + filename, 'r')
            line = file.read()
            file.close()
            status = '\nGoodbye'
            msg = line + status
            toaddress = filename
            os.remove(TEMP + filename)
            mailer_func(fromaddress,toaddress,msg,status)
        exit_func()
    except Exception as error:
        errdescr = type(error).__name__ + '\n' + traceback.format_exc()
        logger.info(errdescr)
        error_func(errdescr)

def mailer_func(fromaddress,toaddress,msg,status):
    '''
    This function will produce an email
    '''
    try:
        logger.info('"Starting the mailer"')
        smtp_object=smtplib.SMTP(smtpserver, int(SMPTPORT))
        smtp_object.ehlo()
        smtp_object.starttls()
        smtp_object.login(SESUSR,SESPASS)
        smtp_object.sendmail(fromaddress, toaddress, msg)
        smtp_object.quit
        logger.info('Mailer completed')
    except Exception as error:
        errdescr = type(error).__name__ + '\n' + traceback.format_exc()
        logger.info(errdescr)
        exit_func()

def exit_func():
    '''
    This function is just to exit the lambda script
    '''
    return {'statusCode': 200,'body': json.dumps(status)}
