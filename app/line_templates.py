from linebot.models import (
    CarouselTemplate, CarouselColumn, URITemplateAction, PostbackTemplateAction, MessageTemplateAction, ConfirmTemplate,
    ButtonsTemplate
)


def make_template_action(action_type, label, uri=None, data=None, text=None):
    if action_type == 'uri':
        return URITemplateAction(label=label, uri=uri)
    elif action_type == 'postback':
        if text:
            return PostbackTemplateAction(label=label, data=data, text=text)
        else:
            return PostbackTemplateAction(label=label, data=data)
    elif action_type == 'message':
        return MessageTemplateAction(label=label, text=text)


def make_carousel_column(title, text, actions, thumbnail_image_url):
    if thumbnail_image_url:
        return CarouselColumn(title=title, text=text, actions=actions, thumbnail_image_url=thumbnail_image_url)
    else:
        return CarouselColumn(title=title, text=text, actions=actions)


def make_carousel_template(carousel_columns):
    return CarouselTemplate(columns=carousel_columns)


def make_confirm_template(text, actions):
    return ConfirmTemplate(text=text, actions=actions)


def make_buttons_template(title, text, actions, thumbnail_image_url):
    if thumbnail_image_url:
        return ButtonsTemplate(title=title, text=text, actions=actions, thumbnail_image_url=thumbnail_image_url)
    else:
        return ButtonsTemplate(title=title, text=text, actions=actions)
