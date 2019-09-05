#!/bin/sh

# TODO: if pwd != koel; error and return

# TODO: make sure we're in virtualenv shell

SITE_PACKAGES=$(pipenv --venv)/lib/python3.7/site-packages
DIR=$(pwd)
BUILD_DIR=$(pwd)/build
LAMBDA_ZIP="$BUILD_DIR"/lambda.zip

echo "Creating build folder..."
rm -rf "$BUILD_DIR"
mkdir "$BUILD_DIR"

echo "Installing all packages..."
pipenv install

echo "Installing packages to build folder..."
cd "$SITE_PACKAGES" || exit
zip -r -D "$LAMBDA_ZIP" ./*

echo "Installing source to build folder..."
cd "$DIR" || exit
zip -gr "$LAMBDA_ZIP" config.yaml main.py koel

echo "Creating bucket for python deployment zip..."
aws s3api create-bucket --bucket=koel-lambda-code

echo "Uploading zip to bucket..."
# TODO: parameterize this with a version number
aws s3api put-object --bucket koel-lambda-code --key koel:0.0.1.zip --body build/lambda.zip

echo "Creating cloudformation stack..."
aws cloudformation create-stack \
                  --stack-name koel \
                  --template-body file://cloudformation.yaml \
                  --capabilities CAPABILITY_NAMED_IAM \
                  --parameters ParameterKey=S3Bucket,ParameterValue=koel-lambda-code ParameterKey=S3Key,ParameterValue=koel:0.0.1.zip