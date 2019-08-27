from koel.alerts import Alerter
from koel.config import Config
from koel.parser import Parser
from koel.sms_client import SMSClient

config = Config()

sms_client = SMSClient(config)

parsed_alerts = Parser.parse(config.atom_feed_url)

alerter = Alerter(sms_client, config.filesystem_url, parsed_alerts)
alerter.notify_and_store_alerts()

# TODO:
# tests (mocked)
# project setup stuff
# todos, tests for those todos :)
# error handling/logging (ie: log error and program state when an error occurs)
# see https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html

# cloudformation
# comments, code formatting, README
# deploy

# external resources (cloudformation):

# create a s3 bucket
# create a lambda function
# run lambda on a schedule (cron or otherwise)
