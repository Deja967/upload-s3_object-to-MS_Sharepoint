import configparser
import requests
import json
import os
import boto3
from requests_ntlm2 import HttpNtlmAuth
from datetime import *
from main import *
import email
from requests.auth import HTTPBasicAuth

# def config():
#     config = configparser.ConfigParser()
#     config.read('config.ini')
#     base_path = (config['PATH']['base'])
#     nested_folder = (config['PATH']['site'])
#     username = (config['CREDS']['username'])
#     password = (config['CREDS']['password'])
#     return base_path, nested_folder, username, password


def lambda_handler(event=None, context=None):
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("date and time: ", dt_string)

    # today = date.today()
    # day = today.strftime("%Y-%m-%d")
    # print("Today's Date: ", day)

    # s3 = boto3.client('s3')
    # prefix = "s3_subfolder_name/"
    # bucket = "s3_bucket_name"
    # body = ''

    # response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    # all = response['Contents']
    # latest = max(all, key=lambda x: x['LastModified'])

    # output_file = latest.get('Key')
    # name = output_file.split('s3_subfolder_name')[-1]
    # print(name)

    # s3 = boto3.resource('s3')
    # obj = s3.Object(bucket, output_file)
    # print(obj)
    # modified = obj.last_modified.strftime("%Y-%m-%d")
    # print(modified)

    # body = obj.get()['Body'].read()
    # print("-------body was read-------")

    # msg = email.message_from_bytes(body)

    # for i, part in enumerate(msg.walk(), 1):
    #     if part.get_content_maintype() == 'text/plain':
    #         continue

    #     ct = part.get_content_type()
    #     if ct == 'text/plain':
    #         print("New Mime-part")
    #         print(f"/tcontent-type: {ct}")

    #     filename = part.get_filename()
    #     print(filename)
    #     print("#################")
    #     if filename is None:
    #         pass
    #     filename = f"{filename}"
    #     print(f"\tfilename: {filename}")

    #     extensions = ['.txt', '.rpt']
    #     if filename.endswith(tuple(extensions)):
    #         output_filename = os.path.join('/tmp/' + filename)
    #         print("#######################")
    #         print(output_filename)
    #         print("#######################")
    #         with open(output_filename, 'wb') as fp:
    #             fp.write(part.get_payload(decode=True))
    #             print(f"/tSaving Mime-part to file {output_filename}\n")



        # if you are not using AWS secrets formatting for the sharepoint site is as follows or use the config.ini file to store the credentials or os.environ
        # microsofts API is a bit hard to understand in regards to uploading with the right link. Here you want to have the base site END at the First folder. All other subfolers after it will be in the site variable. Example Below. Note there are other ways you can do it.
        # This is the way I like best that has worked.

        # base_path = "http://my-random-sharepoint-site.com/sites/Folder_One"
        # nested_folder = "/sites/Folder_One/Folder_Two/Folder_Three"

        base_path = "https://dadevlearning.sharepoint.com/sites/dev-learning"
        nested_folder = "/sites/dev-learning/Test"

        username = "deja@dadevlearning.onmicrosoft.com"
        password = "x0A27O81XE57F9"


        # headers = {
        #     'Content-Type': 'application/json; odata=verbose',
        #     'accept': 'application/json; odata=verbose'
        #     }

        # test = requests.get("https://dadevlearning.sharepoint.com/sites/dev-learning/_api/web/GetFolderByServerRelativeUrl('/sites/dev-learning/Test')", auth=HttpNtlmAuth(username, password), headers=headers)
        # print(test)
        # username = "someusername"
        # password = "somepassword"

        # base_path, nested_folder, username, password = config()
        # can use either or
        # username, password, base_path, nested_folder = get_secret()
        requests_post = '{}/_api/web/GetFolderByServerRelativeUrl(\'{}\')/Files/add(url='"\'{}\'"', overwrite=true)'.format(base_path, nested_folder, "Hello.txt")
        file = open("D:\Coding_Projects\Python\Email Parsing\Hi.txt", "rb")

        headers = {
            'Content-Type': 'application/json; odata=verbose',
            'accept': 'application/json; odata=verbose'
        }

        print('Retrieving credentials for: {}'.format(username))

        r = requests.post(f'{base_path}/_api/contextinfo', auth=HttpNtlmAuth(username, password), headers=headers)
        form_digest_value = r.json()['d']['GetContextInformation']['FormDigestValue']
        check = r.json()

        print(json.dumps(check, indent=4, sort_keys=True))
        print("Starting Upload to SharePoint site..")

        headers = {
            'Content-Type': 'application/json; odata=verbose',
            'accept': 'application/json; odata=verbose',
            'x-requestdigest': form_digest_value
        }

        upload_process = requests.post(requests_post, auth=HttpNtlmAuth(username, password), headers=headers, data=file.read())
        print(upload_process)

        if upload_process.status_code != 200:
            print("Error something went wrong. Status code: ", upload_process.status_code)
        else:
            print("Successfully uploaded..")


if __name__ == '__main__':
    # config()
    lambda_handler()


# https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-folders-and-files-with-rest