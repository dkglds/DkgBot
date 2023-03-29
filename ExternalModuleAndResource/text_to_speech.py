""" 文字转语音模块 """
import edge_tts
import asyncio
import uuid
import os


async def gen_speech(text, voice, path) -> None:
    """
    从文字获取对应语音
    :param text: 待转换文字
    :param voice: 使用的声音类型
    :param path: 保存的路径
    :return: 最终语音保存的路径
    """
    name = str(uuid.uuid1()) + '.mp3'
    return_path = os.path.abspath(path) + str(os.path.sep) + name
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(return_path)
    return return_path


if __name__ == '__main__':
    path = asyncio.run(gen_speech('哇，这是一张很可爱的图片！(ﾉ≧∀≦)ﾉ，这是你的宠物吗？', 'zh-CN-XiaoyiNeural', 'resource/voice'))
    print(path)
