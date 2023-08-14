#!/bin/bash
set -ex
export VERSION=$1
export RELEASE_NAME=`basename $GITHUB_REPO`

## Create Release
   export RELEASE_URL=$(curl -H\
  "Authorization: token $SECRET_TOKEN"\
   -d "{\"tag_name\": \"$VERSION\", \"target_commitsh\": \"$VERSION\", \"name\": \"$VERSION\", \"body\": \"Release $VERSION\" }"\
   -H "Content-Type: application/json"\
   -X POST\
   https://api.github.com/repos/$GITHUB_REPO/releases |grep \"url\" |grep releases |sed -e 's/.*\(https.*\)\"\,/\1/'| sed -e 's/api/uploads/')


function create_zip_file() {
  TEMP_DIR=${PWD}/tmp
  mkdir TEMP_DIR
  rm -rf "${TEMP_DIR}"
  cp -- *.tf TEMP_DIR
  cp -r dist/ TEMP_DIR
  cd TEMP_DIR
  zip -r9 "${RELEASE_NAME}.zip" .
  mv "${RELEASE_NAME}".zip ../
  cd ../
  rm -rf TEMP_DIR
}



#### Release package
create_zip_file

### Post the release
curl -X POST -H "Authorization: token $SECRET_TOKEN" --data-binary "@${RELEASE_NAME}.zip" -H "Content-type: application/octet-stream" $RELEASE_URL/assets?name=${RELEASE_NAME}.zip
