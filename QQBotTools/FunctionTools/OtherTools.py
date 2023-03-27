""" doc """
from datetime import datetime, timedelta, timezone


class OtherTools(object):
    """ doc """

    def __init__(self):
        # TODO document why this method is empty
        pass

    @staticmethod
    def get_bj_time():
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
