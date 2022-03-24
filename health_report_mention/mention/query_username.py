from hit.ids import idslogin
import json
from typing import Optional
import datetime
import asyncio


async def get_data(username, password, date: Optional[datetime.date] = None):
    return await asyncio.get_running_loop().run_in_executor(None, _get_data, username, password, date)

def _get_data(username, password, date: Optional[datetime.date] = None):
    if date is None:
        date = datetime.date.today()
    session = idslogin(username, password)
    session.get('https://xg.hit.edu.cn/zhxy-xgzs/common/casLogin?params=L3hnX3lxZ2wveXFma2dsZmR5L2ZkeVhx')
    data = {
        "info": json.dumps({
                'page': 1,
                'pageSize': 200,
                'take': 200,
                'skip': 0,
                "data": {
                    "XH": "",
                    "sffsdx": "",
                    "BS": "wsvrs",
                    "RQ": date.strftime("%Y-%m-%d"),
                },
            })
    }
    resp = session.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_yqgl/yqfkglfdy/listYqxx', data=data, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Referer": 'https://xg.hit.edu.cn/zhxy-xgzs/xg_yqgl/yqfkglfdy/fdyXq'
    })
    return resp.json()['module']['data']