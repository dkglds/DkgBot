""" doc """
import json
import Const

with open(Const.JSON_PATH, "r",encoding="utf-8") as json_file:
    CONFIG = json.load(json_file)
