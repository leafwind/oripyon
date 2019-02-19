from linebot.models import Event


class MemberJoinEvent(Event):
    """Webhook MemberJoinEvent.

    https://developers.line.biz/en/reference/messaging-api/#member-joined-event

    Event object for when a user joins a group or room that the bot is in.
    You can reply to join events.
    """

    def __init__(self, timestamp=None, source=None, reply_token=None, **kwargs):
        """__init__ method.

        :param long timestamp: Time of the event in milliseconds
        :param source: Source object
        :type source: T <= :py:class:`linebot.models.sources.Source`
        :param str reply_token: Reply token
        :param kwargs:
        """
        super(MemberJoinEvent, self).__init__(
            timestamp=timestamp, source=source, **kwargs
        )

        self.type = 'memberJoined'
        self.reply_token = reply_token


class MemberLeaveEvent(Event):
    """Webhook MemberJoinEvent.

    https://developers.line.biz/en/reference/messaging-api/#member-left-event

    Event object for when a user leaves a group or room that the bot is in.
    You can reply to join events.
    """

    def __init__(self, timestamp=None, source=None, reply_token=None, **kwargs):
        """__init__ method.

        :param long timestamp: Time of the event in milliseconds
        :param source: Source object
        :type source: T <= :py:class:`linebot.models.sources.Source`
        :param str reply_token: Reply token
        :param kwargs:
        """
        super(MemberLeaveEvent, self).__init__(
            timestamp=timestamp, source=source, **kwargs
        )

        self.type = 'memberLeft'
        self.reply_token = reply_token

