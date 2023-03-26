import pickle

class ChatCompletion:
    api_key = 0
    @classmethod
    def create(cls, model, messages):
        with open(r"C:\Users\86188\Documents\GitHub\DkgBot\GPTTools\MyOpenAi\gptTestFile\resp.dat","rb") as f:
            respData = pickle.load(f)
            respData["choices"][0]["message"]["content"] = \
            "你使用的key为：{0}\n" \
            "你调用的模型为：{1}\n" \
            "你发送的消息队列为：".format(cls.api_key,model)
            for eachMessage in messages:
                respData["choices"][0]["message"]["content"] += "\n" + str(eachMessage)
            """
            {
              "choices": [
                {
                  "finish_reason": "stop",
                  "index": 0,
                  "message": {
                    "content": "\u4f60\u597d\u3002",
                    "role": "assistant"
                  }
                }
              ],
              "created": 1679818864,
              "id": "chatcmpl-6yFuaIEGVdVfFJJeUyEdszOULcoq3",
              "model": "gpt-3.5-turbo-0301",
              "object": "chat.completion",
              "usage": {
                "completion_tokens": 3,
                "prompt_tokens": 26,
                "total_tokens": 29
              }
            }
            """
        return respData
