""" 角色信息模块 """
import json
from Config.Config import CONFIG

# 读取配置信息
with open(CONFIG["chatgpt"]["roles"], "r", encoding="utf-8") as json_file:
    ROLES = json.load(json_file)
