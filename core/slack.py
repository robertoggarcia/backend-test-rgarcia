from django.conf import settings
from django.contrib.sites.models import Site
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def send_slack_message(menu_id):
    """Send slack message
    Args:
        menu_id (uuid4): Menu id to send
    """
    client = WebClient(token=settings.SLACK_TOKEN)
    site = Site.objects.get_current()
    url = f'https://{site.domain}/menu/{menu_id}/'
    message = f"Hello! I share today's menu : {url}"

    try:
        response = client.chat_postMessage(
            channel=settings.SLACK_CHANNEL,
            text=message
        )
        assert response["message"]["text"] == message
        return message
    except SlackApiError as e:
        raise Exception(f"Got an error: {e.response['error']}")
