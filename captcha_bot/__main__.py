import structlog

from telegrinder import API, Dispatch, HTMLFormatter, Telegrinder, Token as BotToken

from captcha_bot.dispatchers import new_joiner
from captcha_bot.utils import BOT_TOKEN


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
)

logger = structlog.get_logger()

api = API(token=BotToken(BOT_TOKEN))
api.default_params["parse_mode"] = HTMLFormatter.PARSE_MODE

dp = Dispatch()
bot = Telegrinder(api, dispatch=dp)

for handler in [new_joiner]:
    logger.debug(
        "Loading handler. Views count",
        handler=handler,
        views_count=len(handler.dp.get_views()),
    )

    dp.load(handler.dp)


# async def init_database() -> None:


# async def on_startup() -> None:
#     await init_database()


# @bot.loop_wrapper.lifespan.on_startup
# async def lifespan_on_startup() -> None:
#     await on_startup()


bot.run_forever(skip_updates=True)
