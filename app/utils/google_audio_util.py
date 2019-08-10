from linebot.models import (
    AudioSendMessage
)


def get_google_audio_url(query):
    stream_url = f'https://google-translate-proxy.herokuapp.com/api/tts?query={query}&language=zh-tw'
    return stream_url


def get_google_audio_message(query):
    url = get_google_audio_url(query)
    audio_send_message = AudioSendMessage(
        original_content_url=url,
        duration=len(query)*1000//3  # chinese character has 3 bytes
    )
    return audio_send_message
