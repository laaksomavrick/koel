import feedparser
from typing import List
from koel.alerts import Alert


class Parser:

    @staticmethod
    def parse(url: str) -> List[Alert]:
        alerts = []
        d = feedparser.parse(url)
        entries = d.entries
        for entry in entries:
            alert = Alert(
                id=entry['id'],
                title=entry['title'],
                updated=entry['updated'],
                published=entry['published'],
                summary=entry['summary']
            )
            alerts.append(alert)
        return alerts
