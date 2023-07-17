def _etags_match(etag_object1: dict, etag_object2: dict) -> bool:
  if etag_object1['etag'] != etag_object2['etag']:
    print(f'Mismatching checksums:\n{etag_object1}\n{etag_object2}')
    return False
  else:
    return True
  
def build_match_error(build1, build2):
  if build1 == build2:
    print('Cannot compare the same build')
    exit(1)

def checksum_error(build_1_etags, build_2_etags):
  etags_match_results = []
  for i in range(len(build_1_etags)):
    etags_match_results.append(_etags_match(build_1_etags[i], build_2_etags[i]))
  if False in etags_match_results:
    exit(1)

def file_name_error(build1, build2, build1_files, build2_files):
    if build1_files != build2_files:
      print('File paths do not match')
      print(f'Build {build1}:')
      [print(file_name) for file_name in build1_files]
      print(f'Build {build2}:')
      [print(file_name) for file_name in build2_files]
      exit(1)

def file_count_error(build1, build2, build1_keys, build2_keys):
    if len(build1_keys) != len(build2_keys):
      print('Builds do not contain the same number of files')
      print(f'Build {build1}: {len(build1_keys)} ')
      [print(key) for key in build1_keys]
      print(f'Build {build2}: {len(build2_keys)}')
      [print(key) for key in build2_keys]
      exit(1)
