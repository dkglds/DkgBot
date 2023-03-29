""" CQ码转换模块 """


def cq_image_str(pic_path):
    """ 图片路径转图片发送CQ码 """
    return "[CQ:image,file=" + pic_path + "]"


def cq_voice_str(voice_path):
    """ 声音路径转语音发送CQ码 """
    return "[CQ:record,file=file://" + voice_path + "]"
