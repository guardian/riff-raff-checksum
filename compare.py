import sys
from aws import *
from error_checks import *
import boto3
import os

project, b1, b2 = str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

def _strip_prefixes(build: int, ls: list[str]) -> str:
  return [string.replace(f'{project}/{build}/', '') for string in ls]

def compare(project: str, b1: int, b2: int):

  print('Creating S3 client')
  s3Client = boto3.client(
    's3',
    'eu-west-1',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.environ.get('AWS_SESSION_TOKEN'))

  print('Verifying that builds are different')
  build_match_error(b1, b2)

  print('Getting file keys')
  b1_keys, b2_keys = get_keys(project, b1, s3Client), get_keys(project, b2, s3Client)
  file_count_error(b1, b2, b1_keys, b2_keys) # Fail if builds do not contain the same number of files

  print('Verifying file names match')
  b1_files, b2_files = _strip_prefixes(b1, b1_keys), _strip_prefixes(b2, b2_keys)
  file_name_error(b1, b2, b1_files, b2_files) # Fail if file paths do not match

  print('Verifying checksums')
  build_1_etags, build_2_etags = get_etags(b1_keys, s3Client), get_etags(b2_keys, s3Client)
  checksum_error(build_1_etags, build_2_etags) # Fail if checksums do not match
  print('File names and checksums match')

if __name__ == "__main__":
  print(f'Comparing builds {b1} and {b2} for project {project}')
  compare(project, b1, b2)
