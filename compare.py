import sys
from aws import *
from error_checks import *

project, b1, b2 = str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

def _strip_prefixes(build: int, ls: list[str]) -> str:
  return [string.replace(f'{project}/{build}/', '') for string in ls]

def compare(project: str, b1: int, b2: int):
  build_match_error(b1, b2)

  b1_keys, b2_keys = get_keys(project, b1), get_keys(project, b2)
  file_count_error(b1, b2, b1_keys, b2_keys) # Fail if builds do not contain the same number of files

  b1_files, b2_files = _strip_prefixes(b1, b1_keys), _strip_prefixes(b2, b2_keys)
  file_name_error(b1, b2, b1_files, b2_files) # Fail if file paths do not match

  build_1_etags, build_2_etags = get_etags(b1_keys), get_etags(b2_keys)
  checksum_error(build_1_etags, build_2_etags) # Fail if checksums do not match
  print('File names and checksums match')

if __name__ == "__main__":
  compare(project, b1, b2)
