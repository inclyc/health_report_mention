# nonebot2 get config
from loguru import logger
from nonebot.adapters.onebot.v11 import Bot as ONEBOT_V11Bot
from nonebot import get_driver, get_bot

from health_report_mention.mention.query_username import get_data
from .config import Config
import pandas as pd
from nonebot import require


driver = get_driver()
conf = Config.parse_obj(driver.config)
student_qq_id: pd.DataFrame


@driver.on_startup
async def _():
    global student_qq_id
    # read student qq id with path specified in config file.
    student_qq_id = pd.read_csv(conf.student_qq_id_path, index_col='学号')
    

scheduler = require("nonebot_plugin_apscheduler").scheduler


# 注册11点和下午1点的每日任务
@scheduler.scheduled_job("cron", hour=11, minute=0)
async def _():
    await main_task()


@scheduler.scheduled_job("cron", hour=13, minute=0)
async def _():
    await main_task()



# @scheduler.scheduled_job("cron", second='*/10')
# async def _():
#     await main_task()


async def try_send_private_msg(user_id: int, message: str) -> None:
    if conf.dry_run:
        logger.success("dry run, {}: {}", user_id, message)
        return
    bot: ONEBOT_V11Bot = get_bot()  # type: ignore 
    logger.success("Sending message {} to {}", message, user_id)
    await bot.send_private_msg(user_id=user_id, message=message)

async def main_task():
    try:
        should_mention = [x['XH'] for x in await get_data(conf.username, conf.password)]
    except Exception as e:
        logger.exception(f"{e!r}")
        return
    for xh in should_mention:
        try:
            qq = student_qq_id.loc[xh]['QQ']
        except KeyError:
            logger.warning(f"{xh} not found in student_qq_id.csv")
            continue
        except Exception as e:
            logger.exception(f"{e!r}")
            continue
        await try_send_private_msg(user_id=int(qq), message="每日上报！") # type: ignore