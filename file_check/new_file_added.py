import boto3
from datetime import *
import pandas as pd
from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay
from holiday_calendar import *
import numpy
from region_two import *


def lambda_handler(event=None, context=None):
    # Grabbing the latest added file from an AWS S3 bucket in a sub-folder and comparing the dates to the current date.
    today = date.today()
    day = today.strftime("%Y-%m-%d")
    print("Today's Date: ", day)

    s3 = boto3.client('s3')
    prefix = "s3_subfolder_name/"
    bucket = "s3_bucket_name"

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    all = response['Contents']
    latest = max(all, key=lambda x: x['LastModified'])


    # The three lines above spit out json so here is where we grab the specific key we want which is 'Key' for an S3 onject
    # When an s3 object is grabbed this way we should split the key value and only include the actual object filename

    output_file = latest.get('Key')
    name = output_file.split('s3_subfolder_name')[-1]
    print(name)

    s3 = boto3.resource('s3')
    obj = s3.Objecct(bucket, output_file)
    print(obj)

    # In AWS S3 buckets, objects are listed "last modified" in a Y-m-d-s format, adding seconds will break the code since seconds rapidly grow.
    # So seconds is split off and we compare today's date in the format Y-m-d to an s3 objects last modified Y-m-d
    modified = obj.last_modified.strftime("%Y-%m-%d")
    print(modified)

    # By comparing the dates we can now see if a file was added on the current day or not
    #
    if modified != day:
        print("No new file added into bucket located in region 1 today")
        result = ("Last modified file: " + str(obj) + " on: " + str(modified))
        print(result)
        print("checking bucket in secondary region")
        print("######################################################################################")
        region_two()
    else:
        print("New file was added into region one today!")
    print("##########################################################################################")


if __name__ == "__main__":
    lambda_handler()
