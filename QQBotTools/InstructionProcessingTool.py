""" doc """


import Const


class InstructionProcessingTool(object):
    """ doc """

    def __init__(self, session_tool):
        self.session_tool = session_tool
        self.message_json = None
        self.return_str = ""

    def process_instruction(self, message_json):
        self.message_json = message_json
        message = message_json.get('raw_message')
        uid = message_json.get('sender').get('user_id')
        return Const.FAILING
