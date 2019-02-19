import json
from linebot.webhook import WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent, UnfollowEvent, JoinEvent, LeaveEvent, PostbackEvent, BeaconEvent
from app.linebot_model_event_extension import MemberJoinEvent, MemberLeaveEvent
from linebot.utils import LOGGER

class WebhookParserExtended(WebhookParser):

    def __init__(self, channel_secret):
        super(WebhookParserExtended, self).__init__(
            channel_secret=channel_secret
        )

    def parse(self, body, signature):
        """Parse webhook request body as text.

        :param str body: Webhook request body (as text)
        :param str signature: X-Line-Signature value (as text)
        :rtype: list[T <= :py:class:`linebot.models.events.Event`]
        :return:
        """
        if not self.signature_validator.validate(body, signature):
            raise InvalidSignatureError(
                'Invalid signature. signature=' + signature)

        body_json = json.loads(body)
        events = []
        for event in body_json['events']:
            event_type = event['type']
            if event_type == 'message':
                events.append(MessageEvent.new_from_json_dict(event))
            elif event_type == 'follow':
                events.append(FollowEvent.new_from_json_dict(event))
            elif event_type == 'unfollow':
                events.append(UnfollowEvent.new_from_json_dict(event))
            elif event_type == 'join':
                events.append(JoinEvent.new_from_json_dict(event))
            elif event_type == 'leave':
                events.append(LeaveEvent.new_from_json_dict(event))
            elif event_type == 'postback':
                events.append(PostbackEvent.new_from_json_dict(event))
            elif event_type == 'beacon':
                events.append(BeaconEvent.new_from_json_dict(event))
            elif event_type == 'memberJoined':
                events.append(MemberJoinEvent.new_from_json_dict(event))
            elif event_type == 'memberLeft':
                events.append(MemberLeaveEvent.new_from_json_dict(event))
            else:
                LOGGER.warn('Unknown event type. type=' + event_type)

        return events


class WebhookHandlerExtended(WebhookHandler):
    """Webhook Handler."""

    def __init__(self, channel_secret):
        """__init__ method.

        :param str channel_secret: Channel secret (as text)
        """
        super(WebhookHandlerExtended, self).__init__(
            channel_secret=channel_secret
        )
        self.parser = WebhookParserExtended(channel_secret)