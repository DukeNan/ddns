import logging.config
from pathlib import Path
from datetime import datetime

LOGO = """
      _     _ 
     | |   | |               Dynamically Updating DNS
   __| | __| |_ __  ___     
  / _` |/ _` | '_ \/ __|     Documents:
 | (_| | (_| | | | \__ \ 
  \__,_|\__,_|_| |_|___/     https://github.com/DukeNan/ddns.git

"""

# aliyun config
ACCESS_KEY_ID = 'xxxxxxxxxx'
ACCESS_KEY_SECRET = 'xxxxxxxxxx'

# domain
DOMAIN = 'aaa.com'
RECORD_ID = '1234567890'  # 域名的RecordId

# log
LOGGING_DIR = Path(__file__).parent / 'logs'
if not LOGGING_DIR.exists():
    LOGGING_DIR.mkdir(parents=True)

LOG_FILENAME = LOGGING_DIR / f'{datetime.now().strftime("%Y%m%d")}.log'

LOGGING = {
    'version': 1,
    # 可否重复使用之前的logger对象
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(levelname)s: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s - %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {  # 定义了一个名为django的日志器
            'handlers': ['file', 'console'],
            'level': 'DEBUG',  # 总级别
            'propagate': True,  # 向上（更高level的logger）传递
        },
    }
}
logging.config.dictConfig(LOGGING)
