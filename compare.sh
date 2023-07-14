#!/usr/bin/env bash

set -e

readonly PROJECT=$1
readonly BUILD_1=$2
readonly BUILD_2=$3
readonly BUCKET=riffraff-artifact

if   [ "$BUILD_1" = "$BUILD_2" ]
   then echo "Error: build numbers are the same!" && exit 1
elif [[ -z "$BUILD_1" || -z "$BUILD_2" || -z "$PROJECT" ]]
   then echo "Missing an argument, expecting input of riff-raff project name, and two built numbers, ie STACK::APP 8 9"  && exit 1
fi

# takes build number as argument, names of all the keys in the build prefix
get_object_names () { aws s3 ls s3://"${BUCKET}/${PROJECT}/$1"/ --profile $PROFILE --recursive --no-paginate | awk '{print $4}' | sort;}

# takes build space or newline separated object list as argument, returns checksums of all keys in build prefix
write_checksums_to_file () {
  SUMS=$(echo $1 | tr -s ' ' '\n' | xargs -L1 aws s3api head-object --bucket ${BUCKET} --profile $PROFILE --region eu-west-1 --query ETag --key)
  echo "$SUMS"
}

OBJECTS_1=$(get_object_names "$BUILD_1")
OBJECTS_2=$(get_object_names "$BUILD_2")

SUMS_1=$(write_checksums_to_file "$OBJECTS_1")
SUMS_2=$(write_checksums_to_file "$OBJECTS_2")

if [[ -z "$SUMS_1" || -z "$SUMS_2" ]]
   then echo "Error: No artifacts found for at least one build" && exit 1
fi

[[ "$SUMS_1" == "$SUMS_2" ]] && echo "Checksums and names of artifacts match" || echo "Checksums and/or of artifacts DO NOT match" && exit 1
#Do object (with stripped prefixes) names match too?
