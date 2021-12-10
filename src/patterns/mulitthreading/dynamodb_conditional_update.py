import boto3,os
from boto3.dynamodb.conditions import Key
import argparse
from datetime import datetime
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr, AttributeNotExists

datasource = 'flight-19096'
partition_key = '20200428'
table_name = 'ygpp-devl-ingestion-notification'

def get_boto3_resource(service='s3'):
    session = boto3.session.Session()
    return session.resource(service)

def get_item():
    dynamodb = get_boto3_resource('dynamodb')
    table = dynamodb.Table(table_name)
    resp = table.get_item(
        Key={
            'datasource': datasource,
            'partitionkey': partition_key,
        }
    )

    print(resp)


def update(col_name, col_val):
    dynamodb = get_boto3_resource('dynamodb')
    table = dynamodb.Table(table_name)

    resp = table.update_item(
        Key={
            'datasource': datasource,
            'partitionkey': partition_key,
        },
        UpdateExpression="set " + col_name + " = :value",
        ExpressionAttributeValues={
            ':value': col_val
        },
        ReturnValues="UPDATED_NEW"
    )

    print(resp)

'''
S3 versioning is enabled.
It is possible for multiple ingestion updates  to come in for the same partition key,
using the S3 version tag, only update if incoming ingestion trigger is for the latest version. 
This is happening in a scenario wherein the downstream is doing some kind of processing 
which is causing 100's of S3 trigger's simultaneously in some instances, so validation was failing as 
lambda was using the older version of the file.

The best solution is to fix at the downstream end, but consumer does not have control
over this at this time. Other solution is to schedule a a lambda S3 pull, instead s3 trigger,
if the processing happens at a particular time, like market closing, etc.

'''
def update_with_condition(col_name, col_val, ver_val):
    dynamodb = get_boto3_resource('dynamodb')
    table = dynamodb.Table(table_name)
    try:
        resp = table.update_item(
            Key={
                'datasource': datasource,
                'partitionkey': partition_key,
            },
            UpdateExpression = "set " + col_name + " = :value, ver = :ver",
            # attribute does not exist or the new version just come in is older the existing version ib dyanmodb
            ConditionExpression= ' attribute_not_exists(ver) or  :ver > ver ',
            ExpressionAttributeValues={
                ':value' : col_val,
                ':ver' : ver_val
            },
            ReturnValues="UPDATED_NEW"
        )
        print(resp)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print(e.response['Error'])


'''
The following code is to test dynamodb conditional update
works as desired when multiple updates happen on the same row/record
'''

import threading

col_checksumver = 'checksumver'
col_ver = 'valueofver'

def worker(col_name, col_val, ver):
    """thread worker function"""
    update_with_condition(col_name, col_val, ver)
    return

'''
Once the threads are started(t.start()) one cannot say which thread will run to completion first.
'''
def run():
    threads = []
    for i in range(40, 20, -2):
        print(str(i) + '...')
        t = threading.Thread(target=worker, args=(col_checksumver + str(i), col_ver + str(i) + " " + datetime.now().strftime('%Y%m%d%H%M%S%f'), i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join() # wait for the thread to complete

    # see the update
    print('get item')
    get_item()


if __name__ == '__main__':
    run()
