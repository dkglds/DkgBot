""" 配置信息模块 """
import json
import Config.Const as Const
import os

# 读取配置信息
with open(Const.JSON_PATH, "r", encoding="utf-8") as json_file:
    CONFIG = json.load(json_file)
