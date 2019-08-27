import json
import unittest
from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

from koel.alerts import Alert, AlertStorage


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


class AlertStorageTests(unittest.TestCase):

    def test_read_storage(self):
        alerts_dict = {
            "tag:weather.gc.ca,2013-04-16:20190822014505": {
                "id": "tag:weather.gc.ca,2013-04-16:20190822014505",
                "title": "No alerts in effect, London - Middlesex",
                "updated": "2019-08-22T01:45:05Z",
                "published": "2019-08-22T01:45:05Z",
                "summary": "No alerts in effect"
            }
        }
        alerts_string = json.dumps(alerts_dict)
        with patch('builtins.open', mock_open(read_data=alerts_string)):
            alerts = AlertStorage.read_storage("foo")
            alert = alerts['tag:weather.gc.ca,2013-04-16:20190822014505']
            self.assertIsNotNone(alert)
            self.assertIsInstance(alert, Alert)

    def test_write_storage(self):
        alerts_log = {
            "tag:weather.gc.ca,2013-04-16:20190822014505": Alert(
                id="id", title="title", updated="updated", published="published", summary="summary"
            )
        }
        fs_path = "foo"
        with patch('builtins.open', new_callable=mock_open()) as mock_file:
            with patch('json.dump') as mock_json:
                AlertStorage.write_storage(fs_path, alerts_log)
                mock_file.assert_called_with(fs_path, 'w')
                mock_json.assert_called_with({
                    "tag:weather.gc.ca,2013-04-16:20190822014505": {
                        "id": "id",
                        "title": "title",
                        "updated": "updated",
                        "published": "published",
                        "summary": "summary",
                    }
                }, mock_file.return_value.__enter__.return_value)

    # TODO if the file doesn't exist, it creates it with an empty {}, then writes

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
