import requests

# Production Campfire URL
# https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#create-a-line
# Posting json data to this URL sends messages to the Campfire chat or whatever in
# the PO Connection project in Basecamp
campfireUrl = "https://3.basecampapi.com/4235635/integrations/Khcgf1FLtqjuiCWtgKdGZov3/buckets/42591593/chats/8723038142/lines"


def send_message(html):
    requests.post(
        campfireUrl,
        json={
            "content": html,
        },
    )
