import requests

import settings

# Production Campfire URL
# https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#create-a-line
# Posting json data to this URL sends messages to the Campfire chat or whatever in
# the PO Connection project in Basecamp


def send_message(html):
    requests.post(
        settings.BASECAMP_CAMPFIRE_URL,
        json={
            "content": html,
        },
    )
