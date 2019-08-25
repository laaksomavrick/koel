from alerts import Alerter
from config import Config
from parser import Parser
from sms_client import SMSClient

config = Config()

sms_client = SMSClient(config)

parsed_alerts = Parser.parse(config.atom_feed_url)

alerter = Alerter(sms_client, config.filesystem_url, parsed_alerts)
alerter.notify_and_store_alerts()

# TODO:
# twilio
# class re-org
# folder re-org
# tests (mocked)
# error handling (ie: log error and program state when an error occurs)
# see https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
# cloudformation
# comments, code formatting, README
# deploy

# external resources (cloudformation):

# create a s3 bucket
# create a lambda function
# run lambda on a schedule (cron or otherwise)
