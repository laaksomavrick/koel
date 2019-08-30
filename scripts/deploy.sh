#!/bin/sh

# Create a zip archive of koel and its dependencies
rm -rf ./build
mkdir ./build
pipenv lock -r > build/requirements.txt
pipenv run pip download -d ./build/vendor -r ./build/requirements.txt
zip -r build/lambda.zip build/vendor
zip -gr build/lambda.zip koel
zip -g build/lambda.zip main.py
zip -g build/lambda.zip config.yaml

# Create a bucket specifically for our lambda functions
aws s3api create-bucket --bucket=koel-lambda-code

# Upload our lambda function to that bucket
# TODO: paramaterize this with a version number
aws s3api put-object --bucket koel-lambda-code --key koel:0.0.1 --body ./build/lambda.zip

# Create our s3 bucket and lambda
aws cloudformation create-stack \
                  --stack-name koel \
                  --template-body file://cloudformation.yaml \
                  --capabilities CAPABILITY_NAMED_IAM \
                  --parameters ParameterKey=S3Bucket,ParameterValue=koel-lambda-code ParameterKey=S3Key,ParameterValue=koel:0.0.1