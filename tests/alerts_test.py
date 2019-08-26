import unittest
from datetime import datetime
from unittest.mock import MagicMock
from koel.alerts import Alert


class AlertsTests(unittest.TestCase):

    def test_alert_initialization(self):
        alert = Alert(id="id", title="title", updated="updated", published="published", summary="summary")
        self.assertEqual(alert.id, "id")
        self.assertEqual(alert.title, "title")
        self.assertEqual(alert.updated, "updated")
        self.assertEqual(alert.published, "published")
        self.assertEqual(alert.summary, "summary")

    def test_alert_published_date(self):
        alert = Alert(id="id", title="title", updated="updated", published="2019-08-22T01:45:05Z", summary="summary")
        published_date = alert.published_date()
        self.assertIsInstance(published_date, datetime)

    def test_alert_updated_date(self):
        alert = Alert(id="id", title="title", updated="2019-08-22T01:45:05Z", published="published", summary="summary")
        updated_date = alert.updated_date()
        self.assertIsInstance(updated_date, datetime)

    def test_alert_sms(self):
        alert = Alert(id="id", title="title", updated="updated", published="published", summary="summary")
        sms = alert.sms()
        self.assertEqual(sms, alert.summary)


# AlertStorageTests
    # mock fs
    # it can read from a valid json file and return a Dict[str, Alert]
    # it throws when the file doesnt exist for read
    # it can write to a json file
    # if the file doesn't exist, it creates it with an empty {}, then writes

# AlerterTests
    # if alert is new, it sends and stores
    # if alert is updated, it sends and stores
    # if alert is not updated, it does nothing

# ParserTests
    # it returns a list of Alerts (mock feedparser.parse)
    # if no entries, does nothing

# SmsClientTests
    # sends for each to_number
    # sends from proper from_number
