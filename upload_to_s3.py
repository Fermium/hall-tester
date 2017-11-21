import os
import zipfile
import boto3

product_id = 'ltk-hall'
bucket_name = 'fermiumlabs-manufacturing-data'

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
try:
    last=max([int(obj.key.split('/')[1]) for obj in bucket.objects.all() if obj.key.split('/')[1].isdigit() and obj.key.split('/')[0]==product_id ])

except Exception as e:
    last = 0
import glob
for asset in glob.glob("assets/**/*"):
    bucket.put_object(Key=os.path.join(product_id,asset.replace('assets',str(last+1))), Body=open(asset,'rb'))
