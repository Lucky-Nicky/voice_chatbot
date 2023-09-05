# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#   合成小语种需要传输小语种文本、使用小语种发音人vcn、tte=unicode以及修改文本编码方式
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
from utils.log_util import logger
from userconfig import get_user_conf
from pathlib import Path

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

curr_dir = Path(__file__).absolute().parent
audio_dir = curr_dir.parent / 'static' / 'audio'
file_format = 'pcm'

class Ws_Param(object):

    # 初始化
    def __init__(self, Text):
        # 读取配置信息
        self.conf = get_user_conf('xunfei_conf')

        self.APPID = self.conf['APPID']
        self.APIKey = self.conf['APIKey']
        self.APISecret = self.conf['APISecret']
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {
            "aue": "lame",
            "sfl": 1,
            "auf": "audio/L16;rate=16000",
            "vcn": self.conf['vcn'],
            "tte": "utf8"
        }
        self.Data = {"status": 2, "text": str(
            base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
        # 使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        # self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(
            signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(
            authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致

        return url



    def content_gpt(context: str, count: int):
        # 收到websocket连接建立的处理
        def on_open(ws):

            def run(*args):
                d = {"common": wsParam.CommonArgs,
                     "business": wsParam.BusinessArgs,
                     "data": wsParam.Data,
                     }
                d = json.dumps(d)
                logger.info("------>开始发送文本数据")

                # mp3_file = audio_dir / f'demo.{file_format}'
                # if mp3_file.exists():
                #     mp3_file.unlink()

                ws.send(d)

            thread.start_new_thread(run, ())

        def on_message(ws, message):
            try:
                message = json.loads(message)

                code = message["code"]
                if code != 0:
                    logger.warning(message)

                sid = message["sid"]
                audio = message["data"]["audio"]
                audio = base64.b64decode(audio)
                status = message["data"]["status"]

                if status == 2:
                    logger.info("ws is closed")
                    ws.close()

                if code != 0:
                    errMsg = message["message"]
                    logger.warning("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
                else:
                    logger.info('正在生成mp3文件...')
                    mp3_file = audio_dir / f'demo{count}.{file_format}'
                    with open(mp3_file, 'ab') as f:
                        f.write(audio)

            except Exception as e:
                logger.warning(f'"receive msg,but parse exception:" {e}')

        # 收到websocket关闭的处理
        def on_close(ws):
            print("### closed ###")

        wsParam = Ws_Param(Text=context)

        websocket.enableTrace(False)
        wsUrl = wsParam.create_url()
        ws = websocket.WebSocketApp(
            wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.on_close = on_close
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})





# 收到websocket错误的处理
def on_error(ws, error):
    logger.error(f"### error: {error}")


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
# def on_open(ws):
#     def run(*args):
#         d = {"common": wsParam.CommonArgs,
#              "business": wsParam.BusinessArgs,
#              "data": wsParam.Data,
#              }
#         d = json.dumps(d)
#         print("------>开始发送文本数据")
#         ws.send(d)
#         # if os.path.exists('./demo.mp3'):
#         #     os.remove('./demo.mp3')
#
#     thread.start_new_thread(run, ())


# if __name__ == "__main__":
    # 测试时候在此处正确填写相关信息即可运行
    # wsParam = Ws_Param(APPID='b7cc766e',
    #                    APISecret='MjcxN2E1NjU0MTczMzBhZWM1M2E2ZTdi',
    #                    APIKey='4a1c38cf60b6e037d0fabc853a81e051',
    #                    Text="Python可以用来做什么")
    # websocket.enableTrace(False)
    # wsUrl = wsParam.create_url()
    # ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    # ws.on_open = on_open
    # ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
