import logging

import yaml


class Config:
    """
    Config provides a class which is intended to be a python object representation of the config.yaml
    file, which defines the configuration values for a Koel instance.
    """
    def __init__(self):
        logging.info("Reading config from config.yaml")
        with open("config.yaml", "r") as stream:
            try:
                config = yaml.safe_load(stream)
                self.atom_feed_url = config["atom_feed_url"]
                self.filesystem_url = config["filesystem_url"]
                self.twilio_from_number = config["twilio_from_number"]
                self.twilio_account_sid = config["twilio_account_sid"]
                self.twilio_auth_token = config["twilio_auth_token"]
                self.phone_numbers = config["phone_numbers"]
            except yaml.YAMLError as exc:
                logging.error("An error occurred reading config.", exc_info=True)
