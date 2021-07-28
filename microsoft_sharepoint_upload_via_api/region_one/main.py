import boto3
from botocore.exceptions import ClientError
import json
import base64
import pprint
import os


def get_secret():
    secret_name = 'secret-name (aws provides boiler code already)'
    region = os.environ['AWS_REGION']

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )

    try:
        get_secret_value_response = client.get_secret_value(
            secretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        if e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        if e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
        if e.response['Error']['Code'] == 'AccessDeniedException':
            raise e

        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return secret['user'], secret['pass'], secret['BASE'], secret['SITE']


if __name__ == '__main__':
    get_secret()