import config
import parser
import alerts
from sms_client import SMSClient


config_values = config.read()
atom_feed_url = config_values['atom_feed_url']
filesystem_url = config_values['filesystem_url']

sms_client = SMSClient(config_values)

# todo class Parser
parsed_alerts = parser.parse(atom_feed_url)

alerts.process(sms_client, parsed_alerts, filesystem_url)

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