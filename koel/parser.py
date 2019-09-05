import logging
from typing import List

import feedparser

from koel.alerts import Alert


class Parser:
    """
    Parser provides a class to parse weather alerts from a GC rss feed. Nothing fancy here.
    """
    @staticmethod
    def parse(url: str) -> List[Alert]:
        """
        Parses the given url (which ought to be a GC rss feed url), returning a list of Alerts
        """
        logging.info(f"Parsing alerts from {url}")
        alerts = []
        d = feedparser.parse(url)
        entries = d.entries
        for entry in entries:
            alert = Alert(
                id=entry["id"],
                title=entry["title"],
                updated=entry["updated"],
                published=entry["published"],
                summary=entry["summary"],
            )
            alerts.append(alert)
        return alerts
