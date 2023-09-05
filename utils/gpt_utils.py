import json

import openai
import os

from utils.log_util import logger
from utils.tts_ws_utils import Ws_Param
from userconfig import get_user_conf

context = ""
# def gpt_stream(question):

    # # openai.api_key = os.getenv("OPENAI_API_KEY")
    # # openai.api_key = get_user_conf('openai_api_key')
    # openai.api_key = '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'
    # # print(openai.api_key)
    # global context
    #
    # try:
    #     result = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "user", "content": question},
    #             # {"role": "assistant", "content": context}
    #         ],
    #         temperature=0.7,
    #         stream=True,
    #     )
    #
    #     for chunk in result:
    #         if chunk["choices"][0]["finish_reason"] is not None: # type: ignore
    #             data = "[DONE]"
    #         else:
    #             data = chunk["choices"][0]["delta"].get("content", "") # type: ignore
    #             # context += data
    #         yield "data: %s\n\n" % data.replace("\n", "<br />")
    # except Exception as e:
    #     logger.warning(e)

import openai

# openai.log = "debug"
openai.api_key = get_user_conf('openai_api_key')
# openai.api_key = "sk-L95YXqkGeimdD4gGWJdcxLpuGsB4MoC"
openai.api_base = "https://api.chatanywhere.com.cn/v1"

# 非流式响应
# completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}])
# print(completion.choices[0].message.content)

def gpt_35_api_stream(question):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
        api_key (str): OpenAI API 密钥

    Returns:
        tuple: (results, error_desc)
    """
    messages = [{'role': 'user','content': question}]
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            stream=True,
        )
        completion = {'role': '', 'content': ''}
        # for event in response:
        #     if event['choices'][0]['finish_reason'] == 'stop':
        #         # print(f'收到的完成数据: {completion}')
        #         break
        #     for delta_k, delta_v in event['choices'][0]['delta'].items():
        #         # print(f'流响应数据: {delta_k} = {delta_v}')
        #         completion[delta_k] += delta_v
        #         print(delta_v)
        # messages.append(completion)  # 直接在传入参数 messages 中追加消息
        # return (True, '')
        # return completion['content']
        for chunk in response:
            if chunk["choices"][0]["finish_reason"] is not None: # type: ignore
                data = "[DONE]"
            else:
                data = chunk["choices"][0]["delta"].get("content", "") # type: ignore
                # context += data
            yield "data: %s\n\n" % data.replace("\n", "<br />")
    except Exception as err:
        return (False, f'OpenAI API 异常: {err}')

if __name__ == '__main__':
#     messages = [{'role': 'user','content': '李白是谁，介绍一下'},]
    data_list = list(gpt_35_api_stream('李白是谁，介绍一下'))
    print(data_list)
#

    # return Ws_Param.content_gpt(context)
    # context = ""
# if __name__ == '__main__':
#     print(    gpt_stream("李白是谁？"))
#     data_list = list(gpt_stream("李白是谁？"))
#     print(data_list)