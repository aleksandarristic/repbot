import logging
import os
import re

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from surblclient import surbl, SurblError

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN, name="Domain Reputation Bot")
logger = logging.getLogger(__name__)

lists_map = {
    'ph': 'Phishing',
    'mw': 'Malware',
    'cr': 'Cracking',
    'abuse': 'Spam and abuse'
}


def get_reputation(lookup_text):
    """ Wrapper for surbl client to show pretty messages """
    try:
        domain, lists = surbl.lookup(lookup_text)
    except SurblError as e:
        logger.error(e)
        return f'Error looking up text "{lookup_text}".'

    if not lists:
        return f'Domain "{domain}" is not blacklisted.'
    else:
        response = f'Domain "{domain}" is on the following blacklists:\n'
        for item in lists:
            response += f' - {lists_map[item]}\n'
        return response


@app.message(re.compile(r"^!rep\s.*"))
def rep_check(event, say):
    chan = event['channel']
    text = event['text']
    # always lookup only the portion after "!rep " & try to unslackify
    lookup_text = unslackify(text[5:])
    response = get_reputation(lookup_text)
    logger.info(f'Lookup: "{lookup_text}", Response: "{response}".')
    say(text=response, channel=chan)


@app.event("message")
def handle_message_events(body):
    logger.info(body)


def unslackify(text):
    """ Return raw text portion of rich text for fqdns, urls and emails """
    if text.startswith('<'):
        return text.split('|')[-1][:-1]
    return text


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
