import json
import boto3
from botocore.vendored import requests
from botocore.vendored.requests.auth import HTTPBasicAuth

# es_url =
# username
# password

# Definition
okay_response = {
    'statusCode': 200,
    'body': json.dumps('Hello from Lambda2!')
}
create_response = {
    'statusCode': 201,
    'body': json.dumps('Index Created')
}
fail_response = {
    'statusCode': 501,
    'body': json.dumps('Not Implemented')
}

def lambda_handler(event, context):
    print(event, type(event))
    message = event['headers']['q']
    print('message', message)
    objects = get_chatbot(message)
    if objects['objecta']:
        photo_url = queryES(objects)
        print('photos:', photo_url)
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        },
            'body': json.dumps(photo_url)
        }
        print('succeed')
    else:
        return fail_response


def clean():
    response = requests.delete(es_url)
    return response


def queryES(objects):
    photos = []
    for key in objects:
        if objects[key]:
            url = es_url + '_search?q=' + objects[key]
            response = requests.get(url, auth=HTTPBasicAuth(username, password)).json()
            # print('es response', response)
            for item in response['hits']['hits']:
                # print('item:', item)
                bucket = item['_source']['bucket']
                key = item['_source']['objectKey']
                photoURL = 'https://{0}.s3.amazonaws.com/{1}'.format(bucket, key)
                if photoURL not in photos:
                    photos.append(photoURL)
    return photos

def get_chatbot(message):
    lex = boto3.client('lex-runtime')
    response = lex.post_text(
        botName='photos_search',
        botAlias='photo_search_',
        userId='AWS_Admin',
        inputText=message)
    print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Lex responses successfully')
        return response['slots']
    else:
        print('Lex fails')
        return None
