#!/bin/sh

# Create a zip archive of koel and its dependencies
rm -rf ./build
mkdir ./build
pipenv lock -r > build/requirements.txt
pipenv run pip download -d ./build/vendor -r ./build/requirements.txt
zip -r build/lambda.zip builld/vendor
zip -gr build/lambda.zip koel
zip -g build/lambda.zip main.py

# Create a bucket specifically for our lambda functions
aws s3api put-object --bucket my-lambda-functions --key PullMarketCode --body ./build/lambda.zip

# Upload our lambda function to that bucket

# Create our s3 bucket and lambda
 aws cloudformation create-stack --stack-name koel --template-body file://cloudformation.yaml --capabilities CAPABILITY_NAMED_IAM
