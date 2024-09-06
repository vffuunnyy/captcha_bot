import time

import structlog

from captcha_generator import CaptchaGenerator
from telegrinder import (
    Dispatch,
    Message,
    WaiterMachine,
)
from telegrinder.rules import (
    HasData,
    IsPrivate,
    Text,
)
from telegrinder.types import InputFile

from captcha_bot.utils import get_captcha_markup


logger = structlog.get_logger()

dp = Dispatch()
dp.message.auto_rules.append(IsPrivate())

wm = WaiterMachine()
captcha_generator = CaptchaGenerator("./emojis", gap=15)


@dp.message(Text("/start"))
async def handle_start_command(message: Message) -> None:
    b = time.perf_counter()
    captcha = captcha_generator.generate(5, 3)
    a = time.perf_counter()
    logger.info("Captcha generated", correct=captcha.correct_emoji, elapsed=a - b)

    bot_message = (
        await message.answer_photo(
            InputFile("captcha.png", captcha.image),
            caption="Выберите эмоджи, который <b>есть</b> на картинке",
            reply_markup=get_captcha_markup(captcha, 3),
        )
    ).unwrap()

    cb, _ = await wm.wait(dp.callback_query, (message.ctx_api, bot_message.message_id), HasData())

    if cb.data.unwrap_or_none() == captcha.correct_emoji:
        await cb.answer("Goodness", show_alert=True)
        await message.answer("Great Job!")
        await bot_message.delete()
    else:
        await cb.answer("Wrong", show_alert=True)
        await bot_message.delete()
