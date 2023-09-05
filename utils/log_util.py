import logging
import pathlib


# 绑定绑定句柄到logger对象
logger = logging.getLogger(__name__)


# 设置日志的格式
date_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s ', date_format)

# 文件句柄
log_dir = pathlib.Path(__file__).absolute().parent.parent / 'log'
if not log_dir.exists():
    log_dir.mkdir(parents=True)

file_log_handler = logging.FileHandler(log_dir.joinpath('chat.log'))
file_log_handler.setFormatter(formatter)

# 输出到控制台
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# 绑定绑定句柄到logger对象
logger.addHandler(stream_handler)
logger.addHandler(file_log_handler)

# 设置日志输出级别
logger.setLevel(level=logging.INFO)