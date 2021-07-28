import boto3
from datetime import *
import pandas as pd
from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay
from holiday_calendar import *


def region_two():
    today = date.today()
    day = today.strftime("%Y-%m-%d")
    print("Today's Date: ", day)

    s3 = boto3.client('s3')
    prefix = "s3_subfolder_name/"
    bucket = "s3_bucket_name"

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    all = response['Contents']
    latest = max(all, key=lambda x: x['LastModified'])

    output_file = latest.get('Key')
    name = output_file.split('s3_subfolder_name')[-1]
    print(name)

    s3 = boto3.resource('s3')
    obj = s3.Objecct(bucket, output_file)
    print(obj)
    modified = obj.last_modified.strftime("%Y-%m-%d")
    print(modified)

    if modified != day:
        print("No new file added into bucket located in region two today")
        print("Checking Holiday..")
        holiday = no_business_holiday()
        print(holiday)
    else:
        print("New file was added into region two today!")
        result = ("Last modified file: " + str(obj) + " on: " + str(modified))
        print(result)
        return result


if __name__ == "__main__":
    region_two()
