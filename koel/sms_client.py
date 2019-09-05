import logging

from twilio.rest import Client

from koel.config import Config


class SMSClient:
    """
    SMSClient wraps our Twilio client, providing us an api to send a message
    to a set of phone numbers.
    """
    def __init__(self, config: Config):
        twilio_account_sid = config.twilio_account_sid
        twilio_auth_token = config.twilio_auth_token

        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.from_number = config.twilio_from_number
        self.to_numbers = config.phone_numbers

    def send(self, message: str) -> None:
        """
        Sends a message to all to_numbers.
        """
        for to_number in self.to_numbers:
            logging.info(f"Sending sms to {to_number} from {self.from_number}")
            self.client.messages.create(
                to=to_number, from_=self.from_number, body=message
            )
