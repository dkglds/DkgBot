""" doc """
import edge_tts
import asyncio
import uuid
import os


async def gen_speech(text, voice, path) -> None:
    """ doc """
    name = str(uuid.uuid1()) + '.mp3'
    return_path = os.path.abspath(path) + str(os.path.sep) + name
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(return_path)
    return return_path


if __name__ == '__main__':
    path = asyncio.run(gen_speech('中文语音测试', 'zh-CN-XiaoyiNeural', '/Users/lucent/go-cqhttp/data/voices'))
    print(path)
