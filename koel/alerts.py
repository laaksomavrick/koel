import json
import logging
from dataclasses import dataclass
from typing import Dict, List

import dateutil.parser
from smart_open import open

from koel.sms_client import SMSClient


@dataclass
class Alert:
    """
    Alert defines the shape of an alert for our purposes, and provides some helpful utility functions
    for working against a given alert.
    """
    id: str
    title: str
    updated: str
    published: str
    summary: str

    def published_date(self):
        """
        Get the published_date of an alert as a datetime.
        """
        return dateutil.parser.parse(self.published)

    def updated_date(self):
        """
        Get the updated_date of an alert as a datetime.
        """
        return dateutil.parser.parse(self.updated)

    def sms(self) -> str:
        """
        Get the sms_message for a given alert.
        """
        return self.title


class AlertStorage:
    """
    AlertStorage provides an API for reading and writing from a file store. This can be either a local file,
    or a file in a s3 bucket.
    """
    @staticmethod
    def read_storage(fs_path: str) -> Dict[str, Alert]:
        """
        Read a json file which ought to represent a log of alerts Koel already knows about.
        """
        with open(fs_path) as json_file:
            try:
                storage = {}
                dump = json.load(json_file)
                for alert_id in dump.keys():
                    alert = dump[alert_id]

                    title = alert["title"]
                    updated = alert["updated"]
                    published = alert["published"]
                    summary = alert["summary"]
                    storage[alert_id] = Alert(
                        id=alert_id,
                        title=title,
                        updated=updated,
                        published=published,
                        summary=summary,
                    )
                return storage
            except:
                logging.error(
                    f"An error occurred reading from storage with path: {fs_path}",
                    exc_info=True,
                )

    @staticmethod
    def write_storage(fs_path: str, alerts_log: Dict[str, Alert]):
        """
        Write an alert to a json file representing a log of alerts Koel knows about.
        """
        try:
            # TODO: investigate why we need to call __dict__
            serializable_alerts_log = {}

            for key in alerts_log.keys():
                serializable_alerts_log[key] = alerts_log[key].__dict__

            with open(fs_path, "w") as outfile:
                json.dump(serializable_alerts_log, outfile)
        except:
            logging.error(
                f"An error occurred writing to storage with path: {fs_path} and log: {alerts_log}",
                exc_info=True,
            )

    @staticmethod
    def create_storage(fs_path):
        """
        Create a json file with an empty object. Necessary for first-time Koel instantiation.
        """
        logging.info(f"Creating storage at: {fs_path}")
        with open(fs_path, "w") as file:
            json.dump({}, file)

    @staticmethod
    def storage_exists(fs_path: str) -> bool:
        """
        Check whether the alerts log json file exists or not.
        """
        try:
            open(fs_path, "r")
            logging.info(f"Found storage at: {fs_path}")
            return True
        except:
            logging.info(f"Did not find storage at: {fs_path}")
            return False


class Alerter:
    """
    Alerter provides an API for sending alerts to phone numbers. That is the whole point, after all.
    """
    def __init__(self, sms_client: SMSClient, fs_path: str, alerts: List[Alert]):
        self.sms_client = sms_client
        self.fs_path = fs_path
        # Don't love statically initializing this
        self.alerts_log = AlertStorage.read_storage(fs_path)
        self.alerts = alerts

    def notify_and_store_alerts(self):
        """
        See notify_and_store_alert, except for all alerts.
        """
        for alert in self.alerts:
            self.notify_and_store_alert(alert)

    def notify_and_store_alert(self, alert: Alert):
        """
        We only want to send updates for new weather alerts so as to not spam the user, so we verify that either:
            - an alert has not yet been seen
            - it has been seen, that is has been updated since last being seen

        Meeting either of these conditions means we'll send the list of phone numbers a text with
        the weather alert contents.
        """
        logging.info(f"Processing alert: {alert.id}")
        alert_id = alert.id
        known_alert = alert_id in self.alerts_log

        if known_alert:
            logged_alert = self.alerts_log[alert_id]

            published = logged_alert.published_date()
            updated = alert.updated_date()

            new_alert = updated > published

            if new_alert:
                logging.info(f"New alert for existing entry: {alert_id}")
                self.upsert_alerts_log(alert)
                sms = alert.sms()
                self.sms_client.send(sms)
            else:
                logging.info(f"Old or same alert, doing nothing: {alert_id}")
        else:
            logging.info(f"New alert: {alert_id}")
            self.upsert_alerts_log(alert)
            sms = alert.sms()
            self.sms_client.send(sms)

    def upsert_alerts_log(self, alert: Alert):
        """
        Either insert or update a given alert record.
        """
        self.alerts_log[alert.id] = alert
        AlertStorage.write_storage(self.fs_path, self.alerts_log)
