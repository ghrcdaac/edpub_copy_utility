import os

import boto3
import concurrent.futures

s3_client = boto3.client('s3')
ed_pub_account_id = os.getenv('EDPUB_ACCOUNT_ID')
source_bucket = os.getenv('EDPUB_BUCKET')
destination_bucket = os.getenv('DAAC_BUCKET')
region = os.getenv('REGION')
prefix = os.getenv('DAAC_PREFIX')


def get_keys(paginator, bucket):
    src_iter = paginator.paginate(
        Bucket=bucket,
        Prefix=prefix
    )
    src_keys = set()
    for rsp in src_iter:
        for items in rsp.get('Contents', []):
            src_keys.add(items.get('Key'))

    return src_keys


def scan_ed_pub():
    paginator = s3_client.get_paginator('list_objects_v2')
    src_keys = get_keys(paginator, source_bucket)
    missing_keys = src_keys.difference(get_keys(paginator, destination_bucket))

    responses = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for key in missing_keys:
            futures.append(
                executor.submit(transfer_wrapper, key)
            )

        for future in concurrent.futures.as_completed(futures):
            responses.append(future.result())

    return responses


def transfer_wrapper(key):
    return s3_client.put_object(
        Bucket=destination_bucket,
        Body=s3_client.get_object(Bucket=source_bucket, Key=key).get('Body').read(),
        Key=key
    )


def handle_s3_event_message(event):
    object_key = event.get('Records')[0].get('s3').get('object').get('key')
    return s3_client.copy_object(
        Bucket=destination_bucket,
        CopySource={
            'Bucket': source_bucket,
            'Key': object_key
        },
        Key=object_key
    )


def handler(event, context):
    if event.get('Records', None):
        ret = handle_s3_event_message(event)
    else:
        ret = scan_ed_pub()

    return ret


if __name__ == '__main__':
    pass
