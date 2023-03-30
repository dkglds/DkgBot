""" 信息发送器类 """
import os
import uuid
import asyncio
import requests
import QQBotTools.FunctionTools.CQTools as CQTools

from Config.Config import CONFIG
from ExternalModuleAndResource.text_to_speech import gen_speech
from ExternalModuleAndResource.text_to_image import text_to_image


class InformationSender(object):
    """ 信息发送器类，拥有4个发送方法应对私聊、群聊的文字和图片发送 """
    image_path = CONFIG['qq_bot']['image_path']
    voice = CONFIG['qq_bot']['voice']
    voice_path = CONFIG['qq_bot']['voice_path']
    cqhttp_url = CONFIG['qq_bot']['cqhttp_url']
    max_length = CONFIG['qq_bot']['max_length']

    # 生成图片
    @classmethod
    def gen_img(cls, message):
        """
        文字转图片，调用外部库进行转换
        :param message: 待转换文字字符
        :return: 转换后的文件名
        """
        img = text_to_image(message)
        filename = str(uuid.uuid1()) + ".png"
        filepath = cls.image_path + str(os.path.sep) + filename
        img.save(filepath)
        print("图片生成完毕: " + filepath)
        return filename

    # 发送私聊消息方法 uid为qq号，message为消息内容
    @classmethod
    def send_private_message(cls, uid, message, send_voice):
        """
        发送私聊消息
        :param uid: 目标QQ号
        :param message: 待发送消息
        :param send_voice: 是否发送语音
        :return: 将消息发送信息通过http协议传递给go-cphttp
        """
        if message == "":
            return
        try:
            if send_voice:  # 如果开启了语音发送
                voice_path = asyncio.run(
                    gen_speech(message, cls.voice, cls.voice_path))
                message = CQTools.cq_voice_str(voice_path)
            if len(message) >= cls.max_length and not send_voice:  # 如果消息长度超过限制，转成图片发送
                pic_path = cls.gen_img(message)
                message = CQTools.cq_image_str(pic_path)
            res = requests.post(url=cls.cqhttp_url + "/send_private_msg",
                                params={'user_id': int(uid), 'message': message}).json()
            if res["status"] == "ok":
                print("私聊消息发送成功")
            else:
                print(res)
                print("私聊消息发送失败，错误信息：" + str(res['wording']))

        except Exception as error:
            print("私聊消息发送失败")
            print(error)

    # 发送私聊消息方法 uid为qq号，pic_path为图片地址
    @classmethod
    def send_private_message_image(cls, uid, pic_path, msg):
        """
        发送私聊图片
        :param uid: 目标QQ号
        :param pic_path: 图片路径
        :param msg: 补充消息
        :return: 将消息写为cq码发送信息通过http协议传递给go-cphttp
        """
        try:
            message = CQTools.cq_image_str(pic_path)
            if msg != "":
                message = msg + '\n' + message
            res = requests.post(url=cls.cqhttp_url + "/send_private_msg",
                                params={'user_id': int(uid), 'message': message}).json()
            if res["status"] == "ok":
                print("私聊消息发送成功")
            else:
                print(res)
                print("私聊消息发送失败，错误信息：" + str(res['wording']))

        except Exception as error:
            print("私聊消息发送失败")
            print(error)

    # 发送群消息方法
    @classmethod
    def send_group_message(cls, gid, message, uid, send_voice, message_id):
        """
        发送群聊消息
        :param gid: 目标群号
        :param message: 待发送消息
        :param uid: 目标QQ号
        :param send_voice: 是否发送语音
        :param message_id: 回复的消息id
        :return: 将消息发送信息通过http协议传递给go-cphttp
        """
        if message == "":
            return
        try:
            if send_voice:  # 如果开启了语音发送
                voice_path = asyncio.run(
                    gen_speech(message, cls.voice, cls.voice_path))
                message = CQTools.cq_voice_str(voice_path)
            if len(message) >= cls.max_length and not send_voice:  # 如果消息长度超过限制，转成图片发送
                pic_path = cls.gen_img(message)
                message = CQTools.cq_image_str(pic_path)
            if not send_voice and uid is not None:
                message = str('[CQ:reply,id=%d]\n' % message_id) + \
                          str('[CQ:at,qq=%s]\n' % uid) + \
                          message  # @发言人
            res = requests.post(url=cls.cqhttp_url + "/send_group_msg",
                                params={'group_id': int(gid), 'message': message}).json()
            if res["status"] == "ok":
                print("群消息发送成功")
            else:
                print("群消息发送失败，错误信息：" + str(res['wording']))
        except Exception as error:
            print("群消息发送失败")
            print(error)

    # 发送群消息图片方法
    @classmethod
    def send_group_message_image(cls, gid, pic_path, uid, msg, message_id):
        """
        发送群聊图片
        :param gid: 目标群号
        :param pic_path: 图片路径
        :param uid: 目标QQ号
        :param msg: 补充消息
        :param message_id: 回复的消息id
        :return: 将消息写为cq码发送信息通过http协议传递给go-cphttp
        """
        try:
            message = CQTools.cq_image_str(pic_path)
            if msg != "":
                message = msg + '\n' + message
            message = str('[CQ:reply,id=%d]' % message_id) + \
                      message  # @发言人
            res = requests.post(url=cls.cqhttp_url + "/send_group_msg",
                                params={'group_id': int(gid), 'message': message}).json()
            if res["status"] == "ok":
                print("群消息发送成功")
            else:
                print("群消息发送失败，错误信息：" + str(res['wording']))
        except Exception as error:
            print("群消息发送失败")
            print(error)
