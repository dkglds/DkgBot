""" 配置信息模块 """
import json
import Const

# 读取配置信息
with open(Const.JSON_PATH, "r", encoding="utf-8") as json_file:
    CONFIG = json.load(json_file)
