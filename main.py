from koel.alerts import Alerter, AlertStorage
from koel.config import Config
from koel.parser import Parser
from koel.sms_client import SMSClient
import logging
import sys


def handler(event, context):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info("Booting up koel...")

    config = Config()

    if AlertStorage.storage_exists(config.filesystem_url) is False:
        AlertStorage.create_storage(config.filesystem_url)

    sms_client = SMSClient(config)

    parsed_alerts = Parser.parse(config.atom_feed_url)

    alerter = Alerter(sms_client, config.filesystem_url, parsed_alerts)
    alerter.notify_and_store_alerts()
