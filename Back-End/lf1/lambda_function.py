import json
import boto3
from botocore.vendored import requests
from datetime import datetime
from botocore.vendored.requests.auth import HTTPBasicAuth

# Definition
okay_response = {
    'statusCode': 200,
    'body': json.dumps('OK')
}
create_response = {
    'statusCode': 201,
    'body': json.dumps('Index Created')
}
fail_response = {
    'statusCode': 501,
    'body': json.dumps('Not Implemented')
}
MinConfidence = 90

# elasticsearch path
#es_url = ''
#username = ''
#password = ''

random_seed = '1688'
AWS_REGION = 'us-east-1'


def lambda_handler(event, context):
    print('event', event)
    # key = 'images/put/cat2.jpg'
    # bucket = 'cloud-computing-a2-b2'
    key = event['Records'][0]['s3']['object']['key']  # 'images/Example.jpg'
    bucket = event['Records'][0]['s3']['bucket']['name']  # 'cloud-computing-a2-b2'
    rek_response = detect_labels(bucket, key)
    print(rek_response)
    customized_label = label_handler(key, bucket)
    print('cclabel', customized_label, type(customized_label))
    json_instance = json_wrapper(key, bucket, rek_response, customized_label)
    print('json_wrapper_result:', json_instance)
    es_response = es_insert_index(json_instance, username, password, es_url)
    # es_response_yin = es_insert_index(json_instance, username_yin, password_yin, es_url_yin)
    print('tim es', es_response.text)
    # print('yin es',es_response_yin.text)
    return create_response


def label_handler(key, bucket):
    s3 = boto3.client(
        's3',
        region_name='us-east-1',
        aws_access_key_id='',
        aws_secret_access_key=''
    )
    response = s3.head_object(
        Bucket=bucket,
        Key=key
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200 and response['ResponseMetadata']['HTTPHeaders'][
        'x-amz-meta-customlabels']:
        return response['ResponseMetadata']['HTTPHeaders']['x-amz-meta-customlabels'].split(',')
    else:
        return None


def es_insert_index(json_instance, username, password, url):
    # response = requests.post(es_url, auth=HTTPBasicAuth(username, password), json=json, headers=headers)

    headers = {'Content-Type': 'application/json'}
    index = 'photos'
    type = '_doc'
    url = url + '/' + index + '/' + type
    awsauth = HTTPBasicAuth(username, password)
    response = requests.post(url, auth=awsauth, json=json_instance, headers=headers)
    return response


def json_wrapper(key, bucket, rek_response, assign_labels=None):
    labels = []
    for label in rek_response['Labels']:
        labels.append(label['Name'])
    if assign_labels:
        labels += assign_labels
    json_instance = {
        'objectKey': key,
        'bucket': bucket,
        'createdTimeStamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'labels': labels
    }
    return json_instance


def detect_labels(bucket, key):
    client = boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': key}},
                                    MaxLabels=10, MinConfidence=MinConfidence)
    return response
