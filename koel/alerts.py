import json
from dataclasses import dataclass
from typing import Dict, List

import dateutil.parser

from koel.sms_client import SMSClient


@dataclass
class Alert:
    id: str
    title: str
    updated: str
    published: str
    summary: str

    def published_date(self):
        return dateutil.parser.parse(self.published)

    def updated_date(self):
        return dateutil.parser.parse(self.updated)

    def sms(self) -> str:
        return self.summary


class AlertStorage:
    @staticmethod
    def read_storage(fs_path: str) -> Dict[str, Alert]:
        with open(fs_path) as json_file:
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

    @staticmethod
    def write_storage(fs_path: str, alerts_log: Dict[str, Alert]):
        # TODO: investigate why we need to call __dict__
        serializable_alerts_log = {}

        for key in alerts_log.keys():
            serializable_alerts_log[key] = alerts_log[key].__dict__

        with open(fs_path, "w") as outfile:
            json.dump(serializable_alerts_log, outfile)


class Alerter:
    def __init__(self, sms_client: SMSClient, fs_path: str, alerts: List[Alert]):
        self.sms_client = sms_client
        self.fs_path = fs_path
        # TODO: if it doesn't exist, write {}
        self.alerts_log = AlertStorage.read_storage(fs_path)
        self.alerts = alerts

    def notify_and_store_alerts(self):
        for alert in self.alerts:
            self.notify_and_store_alert(alert)

    def notify_and_store_alert(self, alert: Alert):
        """
        We only want to send updates for new weather alerts so as to not spam the user, so we verify that either:
            - an alert has not yet been seen
            - it has been seen, that is has been updated since last being seen
        Meeting either of these conditions means we'll send the list of phone numbers a text with
        the weather alert contents.

        :param alert: An instance of an alert. See the Alert class.
        :return:
        """
        alert_id = alert.id
        known_alert = alert_id in self.alerts_log

        if known_alert:
            logged_alert = self.alerts_log[alert_id]

            published = logged_alert.published_date()
            updated = alert.updated_date()

            new_alert = updated > published

            if new_alert:
                print("new alert for existing entry")
                self.upsert_alerts_log(alert)
                sms = alert.sms()
                self.sms_client.send(sms)
            else:
                print("old or same alert, doing nothing")
        else:
            print("new alert")
            self.upsert_alerts_log(alert)
            sms = alert.sms()
            self.sms_client.send(sms)

    def upsert_alerts_log(self, alert: Alert):
        self.alerts_log[alert.id] = alert
        AlertStorage.write_storage(self.fs_path, self.alerts_log)
