from captcha_generator import CaptchaData
from envparse import env
from telegrinder import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup


env.read_envfile(".env")

BOT_TOKEN = env.str("BOT_TOKEN")


def get_captcha_markup(captcha: CaptchaData, max_in_row: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboard()
    emojis = captcha.keyboard_emojis
    while emojis:
        while len(kb.keyboard[-1]) < max_in_row and emojis:
            emoji = emojis.pop(0)
            kb.add(
                InlineButton(
                    text=emoji,
                    callback_data=emoji,
                )
            )
        kb.row()
    return kb.get_markup()
