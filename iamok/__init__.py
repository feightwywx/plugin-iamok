import nonebot
from nonebot import require, on_command, permission
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from .config import Config
from .model import construct_msg

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

scheduler = require("nonebot_plugin_apscheduler").scheduler
su_test = on_command("报平安情况", rule=to_me(), priority=5)
        

@scheduler.scheduled_job(
    "cron",
    hour=plugin_config.iamok_report_time_hr,
    minute=plugin_config.iamok_report_time_min,
    id="bpa"
    )
async def report_bpa():
    bot = nonebot.get_bot()
    if plugin_config.iamok_msg_type == "group":
        await bot.send_msg(
            message_type='group',
            group_id=plugin_config.iamok_id,
            message=await construct_msg(plugin_config.iamok_sqlite_path)
        )
    elif plugin_config.iamok_msg_type == "private":
        await bot.send_msg(
            message_type='private',
            user_id=plugin_config.iamok_id,
            message=await construct_msg(plugin_config.iamok_sqlite_path)
        )

@su_test.handle()
async def manual_report(bot: Bot, event: Event, state: T_State):
    await su_test.finish(await construct_msg(plugin_config.iamok_sqlite_path))
