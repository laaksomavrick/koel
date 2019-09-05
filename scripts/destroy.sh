#!/bin/sh

# Delete our stack
aws cloudformation delete-stack --stack-name koel

# Empty our s3 bucket for storing the lambda function zip
aws s3api delete-object --bucket koel-lambda-code --key koel:0.0.1.zip

# Delete our s3 bucket for the lambda function zip
aws s3api delete-bucket --bucket=koel-lambda-code