from twilio.rest import Client

from koel.config import Config


class SMSClient:
    def __init__(self, config: Config):
        twilio_account_sid = config.twilio_account_sid
        twilio_auth_token = config.twilio_auth_token

        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.from_number = config.twilio_from_number
        self.to_numbers = config.phone_numbers

    def send(self, message):
        for to_number in self.to_numbers:
            self.client.messages.create(
                to=to_number, from_=self.from_number, body=message
            )
