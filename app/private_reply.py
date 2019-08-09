from app.common_reply import get_reply_from_mapping_function
from app.rabbit import my_rabbit, adopt_rabbit


pattern_mapping_private = [
    {
        'cmd': '我的兔子',
        'type': 'equal',
        'function': my_rabbit,
        'multi_type_output': True
    },
    {
        'cmd': '領養兔子',
        'type': 'equal',
        'function': adopt_rabbit,
        'multi_type_output': True
    },
]


def private_reply(uid, msg):
    source_id = uid
    reply = get_reply_from_mapping_function(msg, source_id, pattern_mapping_private)
    if reply:
        return reply
