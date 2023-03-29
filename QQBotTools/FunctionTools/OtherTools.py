""" 其他工具模块 """
from datetime import datetime, timedelta, timezone


def get_bj_time():
    """
    获取北京时间
    :return: 当前的北京时间
    """
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )
    # 北京时间
    beijing_now = utc_now.astimezone(SHA_TZ)
    fmt = '%Y-%m-%d %H:%M:%S'
    now_fmt = beijing_now.strftime(fmt)
    return now_fmt
