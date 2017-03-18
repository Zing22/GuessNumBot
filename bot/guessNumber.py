# -*- coding=utf8 -*-

import random

GROUP_NOT_EXIST = 999

guessNumberPool = {} # 用来储存对应的群聊的游戏

class GuessNumber(object):
    def __init__(self, lower, upper=None):
        if not upper:
            upper = lower
            lower = 0
        self.lower = lower
        self.upper = upper
        self.answer = random.randint(lower, upper)
        self.rounds = 0
        # print("新游戏：{l}, {u}, {a}".format(l=self.lower, u=self.upper, a=self.answer))

    def guess(self, g, member):
        if g<self.lower or g>self.upper:
            return -1, "{g} 不在范围哇".format(g=g)
        elif g==self.answer:
            self.rounds += 1
            return 1, "{m}猜中了数字{a}！\n回合数：{r}".format(m=member.name, a=self.answer, r=self.rounds)
        elif g < self.answer:
            self.lower = g+1
            self.rounds += 1
            return 0, "新范围 [{lower}, {upper}]".format(
                        lower=self.lower, upper=self.upper)
        else:
            self.upper = g-1
            self.rounds += 1
            return 0, "新范围 [{lower}, {upper}]".format(
                        lower=self.lower, upper=self.upper)

    def restart(self, lower, upper=None):
        if not upper:
            upper = lower
            lower = 0
        self.lower = lower
        self.upper = upper
        self.answer = random.randint(lower, upper)
        self.rounds = 0

    def __repr__(self):
        return "范围在 [{lower}, {upper}]".format(lower=self.lower, upper=self.upper)


def help():
    res = "发送消息：\n"
    res += "“猜数字 xx” - 开启 0~xx 的新游戏\n"
    res += "“猜数字 xx yy” - 开启 xx~yy 的新游戏\n"
    res += "“zz” - 一轮猜数字\n"
    res += "“范围” - 显示数字范围\n"
    res += "“结束” - 结束游戏\n"
    res += "“帮助” - 查看帮助"
    return res


def newGame(group, lower, upper=None):
    if guessNumberPool.get(group):
        guessNumberPool[group].restart(lower, upper)
    else:
        guessNumberPool[group] = GuessNumber(lower, upper)
    return guessNumberPool[group]


def guess(group, number, member):
    if guessNumberPool.get(group):
        return guessNumberPool[group].guess(number, member)
    else:
        return GROUP_NOT_EXIST, False


# 检查一个字符串是否代表整数
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def checkRaw(group, member, raw):
    # 检查是否是想新建游戏
    cmd = raw.strip().split()
    if len(cmd) == 2 and cmd[0] == "猜数字" and RepresentsInt(cmd[1]) and int(cmd[1]) > 0:
        return newGame(group, int(cmd[1]))
    elif len(cmd) == 3 and cmd[0] == "猜数字" and RepresentsInt(cmd[1]) and RepresentsInt(cmd[2]) \
            and int(cmd[1]) >= 0 and int(cmd[1]) < int(cmd[2]):
        return newGame(group, int(cmd[1]), int(cmd[2]))
    elif len(cmd) == 1 and RepresentsInt(cmd[0]):
        res = guess(group, int(cmd[0]), member)
        if res[0] == 1:
            # 猜中了就结束游戏
            del guessNumberPool[group]
        return res[1]
    elif raw == "帮助":
        return help()
    elif raw == "范围" and guessNumberPool.get(group):
        return guessNumberPool[group]
    elif raw == "结束" and guessNumberPool.get(group):
        del guessNumberPool[group]
        return "猜数字游戏结束"
    else:
        return False