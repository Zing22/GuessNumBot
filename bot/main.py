# -*- coding=utf8 -*-

from wxpy import *
from config import *
import guessNumber

bot = Bot()

@bot.register()
def unknow_msg(msg):
    print('[UNKNOWN]',msg)
    # chat = msg.chat
    # chat.send(UNKNOWN_MSG)


@bot.register(msg_types=TEXT)
def raw_msg_handle(msg):
    # 只支持群聊
    if not isinstance(msg.sender, Group):
        print('[SINGLE]',msg)
        msg.chat.send(NEED_GROUP)
    print(msg)
    res = guessNumber.checkRaw(msg.chat, msg.member, msg.text)
    if res:
        msg.chat.send(res)


# 注册好友请求类消息
@bot.register(msg_types=FRIENDS)
# 自动接受验证信息中包含 'wxpy' 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    if ACCEPT_KEYWORD in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send(ACCEPT_GREETING)

bot.start()