import boto3
s3 = boto3.client('s3')
bucket = 'riffraff-artifact'

def get_keys(project: str, build: int, bucket: str = bucket, s3Client = s3) -> list[str]:
  response = s3Client.list_objects_v2(Bucket=bucket, Prefix=f'{project}/{build}/')
  return sorted([f['Key'] for f in response['Contents']])

def _get_etag(object_path: str, bucket: str = bucket,  s3Client = s3) -> str:
  return s3Client.head_object(Bucket=bucket, Key=object_path)['ETag']

def get_etags(object_names: list[str], bucket: str = bucket,  s3Client = s3):
 return [{'key' : object_path, 'etag' : _get_etag(object_path, bucket, s3Client)}for object_path in object_names]

