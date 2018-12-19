# coding: utf-8
from flask import Flask, render_template, request, abort
from linebot import (
        LineBotApi, WebhookHandler
        )
from linebot.exceptions import (
        InvalidSignatureError, LineBotApiError
        )
from linebot.models import (
        MessageEvent, BeaconEvent, PostbackEvent, TextMessage, TextSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, MessageAction
        )
#app config
import app_env
#controller communication
from telnetlib import Telnet

app = Flask(__name__)

line_bot = LineBotApi(app_env.CHANNEL_TOKEN)
webhook_handler = WebhookHandler(app_env.CHANNEL_SECRET)

@app.route('/', methods=["POST"])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers.get("X-Line-Signature", None)
    if signature is None:
        app.logger.warn("no X-Line-Signature found.")
        abort(400)

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.warn("invalid X-Line-Signature found.")
        abort(400)

    return 'OK'

@app.route('/doge')
def doge():
    return render_template("index.html")

#logging username
def dump_username(source):
    try:
        profile = line_bot.get_profile(source.user_id)
        app.logger.info("user name:{}".format(profile.display_name))
    except LineBotApiError:
        app.logger.warn("could not get username.")

#Webhook event handlers
@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    order = app_env.MESSAGE_KEYWORDS.get(event.message.text, app_env.ORDER_INVALID)
    operate_door(order, event.reply_token)
    dump_username(event.source)

@webhook_handler.add(BeaconEvent)
def handle_beacon(event):
    if event.beacon.hwid == app_env.BEACON_HWID:
        confirm_message = TemplateSendMessage(
                alt_text = app_env.DOOR_APPROACHING,
                template = ConfirmTemplate(
                    text = app_env.DOOR_OPERATION_CONFIRM,
                    actions = [
                        PostbackAction(
                            label = app_env.DOOR_OPEN_REPLY_OK_LABEL,
                            text = app_env.DOOR_OPEN_REPLY_OK,
                            data = str(app_env.ORDER_DOOR_OPEN)
                            ),
                        PostbackAction(
                            label = app_env.DOOR_CLOSE_REPLY_OK_LABEL,
                            text = app_env.DOOR_CLOSE_REPLY_OK,
                            data = str(app_env.ORDER_DOOR_CLOSE)
                            )
                        ]
                    )
                )
        line_bot.reply_message(
                event.reply_token,
                confirm_message
                )
    else:
        pass

@webhook_handler.add(PostbackEvent)
def handle_postback(event):
    data = None
    try:
        data = int(event.postback.data)
    except TypeError:
        pass
    if data is not None and data == app_env.ORDER_DOOR_OPEN:
        operate_door(data, event.reply_token)
    elif data is not None and data == app_env.ORDER_DOOR_CLOSE:
        operate_door(data, event.reply_token)
    else:
        pass
    dump_username(event.source)

#door operations
def operate_door(order, reply_token):
    app.logger.debug("order="+str(order))
    message = ""
    flag = False
    if order != app_env.ORDER_INVALID:
        flag = True
        if order == app_env.ORDER_DOOR_OPEN:
            exec_door_open()
            message = app_env.DONE_DOOR_OPEN
        elif order == app_env.ORDER_DOOR_CLOSE:
            exec_door_close()
            message = app_env.DONE_DOOR_CLOSE
        elif order == app_env.ORDER_DOOR_OPEN_REVERSED:
            exec_door_open_reversed()
            message = app_env.DONE_DOOR_OPEN
        elif order == app_env.ORDER_DOOR_CLOSE_REVERSED:
            exec_door_close_reversed()
            message = app_env.DONE_DOOR_CLOSE
    else:
        pass
    if flag:
        line_bot.reply_message(
                reply_token,
                TextSendMessage(text=message)
                )

#actual door operations
def exec_door_open():
    communicate_controller("-os\n".encode())
    app.logger.debug("door opened.")

def exec_door_close():
    communicate_controller("-cs\n".encode())
    app.logger.debug("door closed.")

def exec_door_open_reversed():
    communicate_controller("-ro\n".encode())
    app.logger.debug("door opened(reversed).")

def exec_door_close_reversed():
    communicate_controller("-rc\n".encode())
    app.logger.debug("door closed(reversed).")

def communicate_controller(command):
    if command.decode() == "-cs\n" or command.decode() == "-os\n" or command.decode() == "-ro\n" or command.decode() == "-rc\n":
        with Telnet("localhost", 8080) as controller:
            app.logger.debug(str(controller.read_until("input.\n".encode())))
            controller.write(command)
            app.logger.debug(str(controller.read_all()))
    else:
        pass

#@app.errorhandler(404)
#def not_found(e):
#    return str(e)
#
if __name__ == "__main__":
    app.run()

