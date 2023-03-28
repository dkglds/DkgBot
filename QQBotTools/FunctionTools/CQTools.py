""" doc """


def cq_image_str(pic_path):
    """ doc """
    return "[CQ:image,file=" + pic_path + "]"


def cq_voice_str(voice_path):
    """ doc """
    return "[CQ:record,file=file://" + voice_path + "]"
