import json
from smart_open import open
import dateutil.parser


# TODO: rewrite as a class, becoming unwieldy
# todo class Alerter

def process(sms_client, alerts, fs_path):
    # Get existing log of alerts
    # TODO: if it doesn't exist, write {}
    alerts_log = _read_json(fs_path)

    # Update log and send sms if any changes
    for alert in alerts:
        _handle(sms_client, alert, alerts_log)

    # Write log
    _write_json(fs_path, alerts_log)


def _handle(sms_client, alert, alerts_log):
    """
    _handle is where the bulk of the application logic lives. We only want to send
    updates for new weather alerts so as to not spam the user, so we verify that either:
        - an alert has not yet been seen
        - it has been seen, that is has been updated since last being seen
    Meeting either of these conditions means we'll send the list of phone numbers a text with
    the weather alert contents.

    :param alert: a dictionary containing weather alert data. The schema for this can be seen in _upsert_alerts_log
    :param alerts_log: a dictionary containing all recorded weather alert data. Likewise, see _upsert_alerts_log
    :return: void, this is a function with side effects
    """
    alert_id = alert['id']
    known_alert = alert_id in alerts_log

    if known_alert:
        logged_alert = alerts_log[alert_id]

        published = dateutil.parser.parse(logged_alert['published'])
        updated = dateutil.parser.parse(alert['updated'])

        new_alert = updated > published

        if new_alert:
            print("new alert for existing entry")
            _upsert_alerts_log(alert, alerts_log)
            sms_client.send(_get_sms_from_alert(alert))
        else:
            print("old or same alert, doing nothing")
    else:
        print("new alert")
        _upsert_alerts_log(alert, alerts_log)
        sms_client.send(_get_sms_from_alert(alert))


def _get_sms_from_alert(alert):
    return alert.summary


def _upsert_alerts_log(alert, alerts_log):
    alerts_log[alert['id']] = {
        "title": alert['title'],
        "updated": alert['updated'],
        "published": alert['published'],
        "summary": alert['summary']
    }


# todo class Storage
def _read_json(fs_path):
    with open(fs_path) as json_file:
        storage = json.load(json_file)
        return storage


def _write_json(fs_path, log):
    with open(fs_path, 'w') as outfile:
        json.dump(log, outfile)
