import config
import parser
import alerts

config_values = config.read()
atom_feed_url = config_values['atom_feed_url']
filesystem_url = config_values['filesystem_url']

parsed = parser.parse(atom_feed_url)

alerts.handle_alerts(parsed, filesystem_url)


# external resources (cloudformation):

    # create a s3 bucket
    # create a lambda function
    # run lambda on a schedule (cron or otherwise)