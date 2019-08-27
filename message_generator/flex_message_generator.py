from linebot.models import (
    MessageAction, BubbleContainer, BoxComponent,
    ButtonComponent, TextComponent, SpacerComponent
)


def build_top_menu_function_card_content(title, text_contents):
    rows = [
        BoxComponent(
            layout='horizontal',
            spacing='sm',
            contents=[
                ButtonComponent(
                    style='secondary',
                    height='sm',
                    color='#95B9B4',
                    action=MessageAction(label=label, text=text),
                )for (label, text) in buttons
            ]
        )for buttons in text_contents
    ]
    container = BubbleContainer(
        direction='ltr',
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(text=title, weight='bold', size='xl'),
            ],
        ),
        footer=BoxComponent(
            layout='vertical',
            spacing='lg',
            contents=[
                BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=rows
                )
            ]
        ),
    )
    return container
