# import time

import os
from flask import Flask, render_template, request, redirect, session, jsonify
import flask
# import userconfig
# import stock_utils
from utils import gpt_utils
import re
from pathlib import Path

from utils.log_util import logger
from utils.tts_ws_utils import Ws_Param

# from flask_sockets import Sockets


app = Flask("我的GPT应用")
# app.secret_key = "sdafffsasdfsafd242332"
app = Flask(__name__, template_folder='templates')


# sockets = Sockets(app)


@app.route("/")
def index():
    # if "username" not in session:
    #     return redirect("/login")

    # path = os.path.dirname(os.path.abspath(__file__))
    # path = path + '/static/audio/'
    # all_files = os.listdir(path)
    # music_list = []
    # for i in all_files:
    #     x = re.findall(r'(.*?).pcm', i)
    #     music_list.append(x[0])

    root_dir = Path(__file__).absolute().parent
    audio_dir = root_dir / 'static' / 'audio'
    musics = list(audio_dir.glob('*.pcm'))
    music_list = sorted([str(p.name) for p in musics])

    return render_template("chatgpt-clone.html", music_list=music_list)


@app.route("/get_audio_list")
def get_audio_list():
    root_dir = Path(__file__).absolute().parent
    audio_dir = root_dir / 'static' / 'audio'
    musics = list(audio_dir.glob('*.pcm'))
    music_list = sorted([str(p.name) for p in musics], key=lambda x:int(x[4:x.index('.')]))
    logger.info(music_list)

    return jsonify(music_list)


# @app.route("/show_quotas", methods=["GET"])
# def show_quotas():
#     if "username" not in session:
#         return redirect("/login")

#     username = session["username"]
#     return userconfig.get_quotas(username)


@app.route("/chatgpt-clone", methods=["POST", "GET"])
def chatgpt_clone():
    # if "username" not in session:
    #     return redirect("/login")
    logger.info('删除历史音频文件。')
    curr_dir = Path(__file__).absolute().parent
    audio_dir = curr_dir / 'static' / 'audio'
    file_format = 'pcm'

    audio_files = audio_dir.glob(f'*.{file_format}')
    for f in audio_files:
        f.unlink()

    # username = session["username"]
    question = request.args.get("question", "")
    # question = str(question).replace('\r','').replace('\n','').replace('\t','') 
    question = str(question).strip()
    question = str(question).strip('。')
    # question = re.sub(r'\s+', ' ', question).strip()
    if question:
        # result = gpt_utils.gpt_stream(question)
        result = gpt_utils.gpt_35_api_stream(question)
        # print(flask.Response(result, mimetype="text/event-stream"))
        return flask.Response(result, mimetype="text/event-stream")
    return "没有内容"

# @app.after_request
# def after_request(response):
#     print(response)
#     # 模拟请求第二个接口
#     with app.test_client() as client:
#         client.post(f'/mp3_play?context="你好"')
#
#     return response

@app.route("/mp3_play", methods=["POST", "GET"])
def mp3_play():
    context = request.args.get("context", "")
    context = context.replace('<br', '')
    count = request.args.get("count", "0")

    logger.info(f'需要生成音频序号是：{count}，文本内容：{context}')
    if context:
        return flask.Response(
            Ws_Param.content_gpt(context, count),
            mimetype="text/html")
    return "没有内容"

    # @app.route("/stock", methods=["GET", "POST"])
    # def stock():
    #     if "username" not in session:
    #         return redirect("/login")
    #     username = session["username"]

    #     data_type = request.args.get("data_type")
    #     stock_code = request.args.get("stock_code")

    #     if data_type == "stock_table":
    #         for try_cnt in range(10):
    #             # 重试机制
    #             try:
    #                 df_stock_table = stock_utils.get_k_data_before_days(stock_code, 30)
    #                 break
    #             except:
    #                 time.sleep(1)
    #                 continue
    #         return df_stock_table.to_html(index=False, classes="table table-striped")

    #     if data_type == "stock_cash_table":
    #         for try_cnt in range(10):
    #             # 重试机制
    #             try:
    #                 df_stock_table = stock_utils.get_stock_cashes(stock_code)
    #                 break
    #             except:
    #                 time.sleep(1)
    #                 continue
    #         return df_stock_table.to_html(index=False, classes="table table-striped")

    #     if data_type == "gpt_cash_output":
    #         for try_cnt in range(10):
    #             # 重试机制
    #             try:
    #                 df_stock_data = stock_utils.get_stock_cashes(stock_code)
    #                 break
    #             except:
    #                 time.sleep(1)
    #                 continue
    #         question = """
    #         分析如下股票的现金数据，进行数据分析，并且给出投资建议: %s
    #         """ % df_stock_data.to_string()

    #         return flask.Response(
    #             gpt_utils.gpt_stream(username, question),
    #             mimetype="text/event-stream")

    #     if data_type == "gpt_output":
    #         for try_cnt in range(10):
    #             # 重试机制
    #             try:
    #                 df_stock_data = stock_utils.get_k_data_before_days(stock_code, 30)
    #                 break
    #             except:
    #                 time.sleep(1)
    #                 continue
    #         question = """
    #         分析如下股票的交易数据，给出收盘价、交易量的趋势分析，并且给出投资建议: %s
    #         """ % df_stock_data.to_string()

    #         return flask.Response(
    #             gpt_utils.gpt_stream(username, question),
    #             mimetype="text/event-stream")

    #     df_stock_codes = stock_utils.get_hs300_stocks()
    #     stock_codes = []
    #     for idx, row in df_stock_codes.iterrows():
    #         stock_codes.append(
    #             {"code": row["code"], "code_name": row["code_name"]})

    #     return render_template("stock.html", stock_codes=stock_codes)

    # @app.route("/login", methods=["GET", "POST"])
    # def login():
    #     message = ""
    #     if request.method == "POST":
    #         username = request.form.get("username")
    #         password = request.form.get("password")
    #         if userconfig.check_user(username, password):
    #             session["username"] = username
    #             return redirect("/")
    #         else:
    #             message = "用户名或者密码错误"
    #     return render_template("login.html", message=message)

    # @app.route("/logout")
    # def logout():
    session.clear()
    return redirect("/login")


app.run(host="0.0.0.0", port=8888, debug=True)
