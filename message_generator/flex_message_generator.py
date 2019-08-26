from linebot.models import (
    MessageAction, BubbleContainer, BoxComponent,
    ButtonComponent, TextComponent, SeparatorComponent
)


def build_top_menu_function_card_content(title, text_contents):
    contents = [
        ButtonComponent(
            style='primary',
            height='sm',
            color='#95B9B4',
            action=MessageAction(label=label, text=text),
        )
        for (label, text) in text_contents
    ]
    container = BubbleContainer(
        direction='ltr',
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(text=title, weight='bold', size='xl'),
                SeparatorComponent(),
                BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=contents
                )
            ],
        ),
    )
    return container
