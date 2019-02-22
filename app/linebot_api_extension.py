from linebot.http_client import HttpClient, RequestsHttpClient
from linebot.api import LineBotApi
from linebot.models.responses import Profile



class LineBotApiExtension(LineBotApi):

    DEFAULT_API_ENDPOINT = 'https://api.line.me'
    def __init__(self, channel_access_token, endpoint=DEFAULT_API_ENDPOINT,
                 timeout=HttpClient.DEFAULT_TIMEOUT, http_client=RequestsHttpClient):
        super(LineBotApiExtension, self).__init__(
            channel_access_token, endpoint=endpoint,
            timeout=timeout, http_client=http_client
        )


    def get_group_member_profile(self, group_id, user_id, timeout=None):
        """Call get group member profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-group-member-profile

        Get user profile information.

        :param str group_id: Group ID
        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, readtimeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = self._get(
            '/v2/bot/group/{group_id}/member/{user_id}'.format(group_id=group_id, user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)