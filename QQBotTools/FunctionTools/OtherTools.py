""" 其他工具模块 """
import time

import requests

from datetime import datetime, timedelta, timezone

from Config.Config import CONFIG


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


def read_partial_information(self, message_json):
	"""
	从信息报文中筛选所需信息
	:param self: 调用者对象
	:param message_json: 收到的信息报文
	:return: 读取、发送者信息、消息类型、原始信息、发送者qq号码
	"""
	self.message_json = message_json
	# 消息发送者的资料
	self.sender = self.message_json.get('sender')
	# 消息类型
	self.message_type = self.message_json.get('message_type')
	# 获取原始信息
	self.message = self.message_json.get('raw_message')
	# 获取信息发送者的 QQ号码
	if self.sender is not None:
		self.uid = self.sender.get('user_id')


def get_credit_summary_by_index(index):
	"""
	查询账户余额
	:param index: api编号:
	:return: 余额值
	"""
	#print(CONFIG['openai']['api_key'][index])
	used = get_user_total_used(CONFIG['openai']['api_key'][index])
	#print(2)
	#print(used)
	return used / 100


'''
def get_user_create_time(api_key):
	""" 获取账号创建时间 """
	url = "https://api.openai.com/v1/organizations/org-WJFz5wM7bz7QnJvef4Q1CfNN/users"
	res = requests.get(url, headers={
		"Authorization": f"Bearer " + api_key
	}, timeout=10).json()
	print(res["members"]["data"][0]["created"])
	return res["members"]["data"][0]["created"]
'''


def get_user_total_used(api_key):
	""" 获取总的使用量 """
	url = "https://api.openai.com/dashboard/billing/usage?start_date=%s&end_date=%s"
	# create_timestamp = get_user_create_time(api_key)
	current_timestamp = time.time()
	url %= timestamp_to_date(current_timestamp, -98), timestamp_to_date(current_timestamp, 2)
	res = requests.get(url, headers={
		"Authorization": f"Bearer " + api_key
	}, timeout=10).json()
	#print(res)
	return res["total_usage"]


def timestamp_to_date(timestamp, offset_days=0, format_str='%Y-%m-%d'):
	""" 将时间戳转换为日期字符串，可以指定偏移天数 """
	timestamp += offset_days * 24 * 3600  # 将时间戳偏移指定天数
	date_str = time.strftime(format_str, time.localtime(timestamp))
	return date_str
