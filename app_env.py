#coding: utf-8
import os
import dotenv

#general config
ORDER_DOOR_OPEN = 7061
ORDER_DOOR_CLOSE = 6551
ORDER_DOOR_OPEN_REVERSED = 8446
ORDER_DOOR_CLOSE_REVERSED = 5599
ORDER_INVALID = 0

DOOR_APPROACHING = "ドア接近を確認しました。"
DOOR_OPERATION_CONFIRM = "ドアを開けますか?"
#DOOR_OPERATION_CANCEL = "キャンセルしました。"
DOOR_OPEN_REPLY_OK = "開ける"
DOOR_CLOSE_REPLY_OK = "閉める"
DOOR_OPEN_REPLY_OK_LABEL = DOOR_OPEN_REPLY_OK
DOOR_CLOSE_REPLY_OK_LABEL = DOOR_CLOSE_REPLY_OK
DONE_DOOR_OPEN = "ドアを開けました。"
DONE_DOOR_CLOSE = "ドアを閉めました。"

MESSAGE_KEYWORDS = {
        "ドアを開けて": ORDER_DOOR_OPEN,
        "ドアを閉めて": ORDER_DOOR_CLOSE,
        "開かずのドアを開けて": ORDER_DOOR_OPEN_REVERSED,
        "開かずのドアを閉めて": ORDER_DOOR_CLOSE_REVERSED,
        "1o": ORDER_DOOR_OPEN,
        "1c": ORDER_DOOR_CLOSE,
        "2o": ORDER_DOOR_OPEN_REVERSED,
        "2c": ORDER_DOOR_CLOSE_REVERSED
        }

#create dotenv path from current dir
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

#load ".env" file
dotenv.load_dotenv(dotenv_path)

#enumerate environment variables below
CHANNEL_TOKEN = os.environ.get("CHANNEL_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")
BEACON_HWID = os.environ.get("BEACON_HWID")

