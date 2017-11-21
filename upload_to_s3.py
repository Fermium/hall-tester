import os
import zipfile
import boto3
import glob


def upload_assets_s3(assetglob, product_id, bucket_name)
    """
    Uploads a directory from the provided glob to S3
    The directory must contain the name "asset"
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    try:
        last=max([int(obj.key.split('/')[1]) for obj in bucket.objects.all() if obj.key.split('/')[1].isdigit() and obj.key.split('/')[0]==product_id ])
    except Exception as e:
        last = 0
    for asset in glob.glob(assetglob):
        destkey = os.path.join(product_id,asset.replace('assets',str(last+1)))
        bucket.put_object(Key=destkey, Body=open(asset,'rb'))
