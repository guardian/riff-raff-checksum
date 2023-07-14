import sys
import boto3

project, b1, b2 = str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
bucket = 'riffraff-artifact'
s3 = boto3.client('s3')

def _etags_match(etag_object1: dict, etag_object2: dict) -> bool:
  if etag_object1['etag'] != etag_object2['etag']:
    print(f'Mismatching checksums:\n{etag_object1}\n{etag_object2}')
    return False
  else:
    return True
  
def _build_match_error(build1, build2):
  if build1 == build2:
    print('Cannot compare the same build')
    exit(1)

def _checksum_error(build_1_etags, build_2_etags):
  etags_match_results = []
  for i in range(len(build_1_etags)):
    etags_match_results.append(_etags_match(build_1_etags[i], build_2_etags[i]))
  if False in etags_match_results:
    exit(1)

def _file_name_error(build1, build2, build1_files, build2_files):
    if build1_files != build2_files:
      print('File paths do not match')
      print(f'Build {build1}:')
      [print(file_name) for file_name in build1_files]
      print(f'Build {build2}:')
      [print(file_name) for file_name in build2_files]
      exit(1)

def _file_count_error(build1, build2, build1_keys, build2_keys):
    if len(build1_keys) != len(build2_keys):
      print('Builds do not contain the same number of files')
      print(f'Build {build1}: {len(build1_keys)} ')
      [print(key) for key in build1_keys]
      print(f'Build {build2}: {len(build2_keys)}')
      [print(key) for key in build2_keys]
      exit(1)

def _get_keys(bucket: str, project: str, build: int, s3Client = s3) -> list[str]:
  response = s3Client.list_objects_v2(Bucket=bucket, Prefix=f'{project}/{build}/')
  return sorted([f['Key'] for f in response['Contents']])

def _get_etag(bucket: str, object_path: str, s3Client = s3) -> str:
  return s3Client.head_object(Bucket=bucket, Key=object_path)['ETag']

def _get_etags(bucket: str, object_names: list[str], s3Client = s3):
 return [{'key' : object_path, 'etag' : _get_etag(bucket, object_path, s3Client)}for object_path in object_names]

def _strip_prefixes(build: int, ls: list[str]) -> str:
  return [string.replace(f'{project}/{build}/', '') for string in ls]

def compare(project: str, b1: int, b2: int):
  _build_match_error(b1, b2)

  b1_keys, b2_keys = _get_keys(bucket, project, b1), _get_keys(bucket, project, b2)
  _file_count_error(b1, b2, b1_keys, b2_keys) # Fail if builds do not contain the same number of files

  b1_files, b2_files = _strip_prefixes(b1, b1_keys), _strip_prefixes(b2, b2_keys)
  _file_name_error(b1, b2, b1_files, b2_files) # Fail if file paths do not match

  build_1_etags, build_2_etags = _get_etags(bucket, b1_keys), _get_etags(bucket, b2_keys)
  _checksum_error(build_1_etags, build_2_etags) # Fail if checksums do not match
  print('File names and checksums match')

if __name__ == "__main__":
  compare(project, b1, b2)
