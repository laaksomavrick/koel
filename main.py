from koel.alerts import Alerter
from koel.config import Config
from koel.parser import Parser
from koel.sms_client import SMSClient
import logging

logging.info("Booting up koel...")

config = Config()

sms_client = SMSClient(config)

parsed_alerts = Parser.parse(config.atom_feed_url)

alerter = Alerter(sms_client, config.filesystem_url, parsed_alerts)
alerter.notify_and_store_alerts()

# TODO:
# todos, tests for those todos :)

# cloudformation
# comments, code formatting, README
# deploy

# external resources (cloudformation):

# create a s3 bucket
# create a lambda function
# run lambda on a schedule (cron or otherwise)
