import json
import unittest
from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch
from koel.alerts import Alert, Alerter, AlertStorage


class AlertsTests(unittest.TestCase):
    def test_alert_initialization(self):
        alert = Alert(
            id="id",
            title="title",
            updated="updated",
            published="published",
            summary="summary",
        )
        self.assertEqual(alert.id, "id")
        self.assertEqual(alert.title, "title")
        self.assertEqual(alert.updated, "updated")
        self.assertEqual(alert.published, "published")
        self.assertEqual(alert.summary, "summary")

    def test_alert_published_date(self):
        alert = Alert(
            id="id",
            title="title",
            updated="updated",
            published="2019-08-22T01:45:05Z",
            summary="summary",
        )
        published_date = alert.published_date()
        self.assertIsInstance(published_date, datetime)

    def test_alert_updated_date(self):
        alert = Alert(
            id="id",
            title="title",
            updated="2019-08-22T01:45:05Z",
            published="published",
            summary="summary",
        )
        updated_date = alert.updated_date()
        self.assertIsInstance(updated_date, datetime)

    def test_alert_sms(self):
        alert = Alert(
            id="id",
            title="title",
            updated="updated",
            published="published",
            summary="summary",
        )
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
                "summary": "No alerts in effect",
            }
        }
        alerts_string = json.dumps(alerts_dict)
        with patch("builtins.open", mock_open(read_data=alerts_string)):
            alerts = AlertStorage.read_storage("foo")
            alert = alerts["tag:weather.gc.ca,2013-04-16:20190822014505"]
            self.assertIsNotNone(alert)
            self.assertIsInstance(alert, Alert)

    def test_write_storage(self):
        alerts_log = {
            "tag:weather.gc.ca,2013-04-16:20190822014505": Alert(
                id="id",
                title="title",
                updated="updated",
                published="published",
                summary="summary",
            )
        }
        fs_path = "foo"

        with patch("builtins.open", new_callable=mock_open()) as mock_file, patch(
            "json.dump"
        ) as mock_json:
            AlertStorage.write_storage(fs_path, alerts_log)
            mock_file.assert_called_with(fs_path, "w")
            mock_json.assert_called_with(
                {
                    "tag:weather.gc.ca,2013-04-16:20190822014505": {
                        "id": "id",
                        "title": "title",
                        "updated": "updated",
                        "published": "published",
                        "summary": "summary",
                    }
                },
                mock_file.return_value.__enter__.return_value,
            )


@patch("koel.alerts.AlertStorage.write_storage")
@patch("koel.alerts.AlertStorage.read_storage")
class AlerterTests(unittest.TestCase):
    def setUp(self):
        self.sms_client = MagicMock()
        self.sms_client.send = MagicMock()

    def test_newly_found_alert(self, mocked_read_storage, mocked_write_storage):
        mocked_read_storage.return_value = {
            "foo": Alert(
                id="some_id",
                title="title",
                updated="2019-08-22T01:45:05Z",
                published="published",
                summary="summary",
            )
        }

        fs_path = "alerts.json"
        alerts = [
            Alert(
                id="some_other_id",
                title="title",
                updated="2019-08-22T01:45:05Z",
                published="published",
                summary="summary",
            )
        ]

        alerter = Alerter(self.sms_client, fs_path, alerts)
        alerter.notify_and_store_alerts()

        self.sms_client.send.assert_called_once()
        mocked_write_storage.assert_called_once()
        self.assertTrue(alerter.alerts_log["some_other_id"] is not None)

    def test_known_alert_updated(self, mocked_read_storage, mocked_write_storage):
        alert_id = "some_id"
        published = "2019-08-22T01:45:05Z"
        new_updated = "2019-09-22T01:45:05Z"
        fs_path = "alerts.json"

        mocked_read_storage.return_value = {
            alert_id: Alert(
                id=alert_id,
                title="title",
                updated=published,
                published=published,
                summary="summary",
            )
        }

        alerts = [
            Alert(
                id=alert_id,
                title="title",
                updated=new_updated,
                published=published,
                summary="summary",
            )
        ]

        alerter = Alerter(self.sms_client, fs_path, alerts)
        alerter.notify_and_store_alerts()

        self.sms_client.send.assert_called_once()
        mocked_write_storage.assert_called_once()
        self.assertTrue(alerter.alerts_log["some_id"].updated == new_updated)

    def test_known_alert_not_updated(self, mocked_read_storage, mocked_write_storage):
        alert_id = "some_id"
        published = "2019-08-22T01:45:05Z"
        fs_path = "alerts.json"

        mocked_read_storage.return_value = {
            alert_id: Alert(
                id=alert_id,
                title="title",
                updated=published,
                published=published,
                summary="summary",
            )
        }

        alerts = [
            Alert(
                id=alert_id,
                title="title",
                updated=published,
                published=published,
                summary="summary",
            )
        ]

        alerter = Alerter(self.sms_client, fs_path, alerts)
        alerter.notify_and_store_alerts()

        self.sms_client.send.assert_not_called()
        mocked_write_storage.assert_not_called()
        self.assertTrue(alerter.alerts_log["some_id"].updated == published)
