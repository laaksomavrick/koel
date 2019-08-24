import json
from smart_open import open
import dateutil.parser

def handle_alerts(alerts, fs_path):
    storage = _get_storage(fs_path)
    for alert in alerts:
        _handle(alert, storage)

def _handle(alert, storage):
    id = alert['id']
    stored = storage[id]

    if stored:
        print("stored")
        # We know about the alert
        # Has it been updated?
        published = dateutil.parser.parse(stored['published'])
        updated = dateutil.parser.parse(alert['updated'])
        new_alert = updated > published

        if new_alert:
            print("new alert")
            # update storage (upsert_storage)
            # send message (send_message)
        else:
            print("old or same alert")
            # do nothing
    else:
        print("not stored")
        # add to storage (upsert_storage)
        # send me a message (send_message)


def _get_storage(fs_path):
    with open(fs_path) as json_file:
        storage = json.load(json_file)
        return storage
