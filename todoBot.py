from botoy import Action, Botoy, GroupMsg
from botoy import decorators as deco
import os
from datetime import datetime, timedelta
from myRegex import re_time

bot = Botoy()
masterQQ = os.environ['targetQQ']


@bot.friend_context_use
def _(ctx):
    # Block msg except from masterQQ
    if str(ctx.FromUin) != masterQQ:
        return
    return ctx

@bot.on_friend_msg
@deco.ignore_botself
def get_msg(ctx):
    action = Action(ctx.CurrentQQ)

    
    m = re_time.match(ctx.Content)
    currentTime = datetime.now()
    msgDate = None  # Year, month, day
    msgTime = None # minute, 
    if(m!=None):
        if(m.group(2) != None and m.group(3) != None):
            action.sendFriendText(ctx.FromUin, "不能同时出现日期和今天明天啦！")
            return
        
        if(m.group(2) == None and m.group(3) == None):
            msgDate = currentTime
        if(m.group(2) != None and m.group(3) == None):
            if(m.group(2) == "明天"):
                msgDate = currentTime + timedelta(days=1)
            if(m.group(2) == "后天"):
                msgDate = currentTime + timedelta(days=2)
            if(m.group(2) == "大后天"):
                msgDate = currentTime + timedelta(days=3)
        else:
            year = 0
            month = 0
            day = 0
            if(m.group(4) != None):
                year = int(m.group(4)[:-1])
            else:
                year = currentTime.year
            if(m.group(5) != None):
                month = int(m.group(5)[:-1])
                print("MONTH GET")
            else:
                month = currentTime.month
                print(m.group(5))
                print("NO MONTH")
            if(m.group(6) != None):
                if(m.group(6)[-1] == '日'):
                    day = int(m.group(6)[:-1])
                else:
                    day = int(m.group(6))
            else:
                day = currentTime.day

            try:
                msgDate = datetime(year, month, day)
            except ValueError as e:
                action.sendFriendText(ctx.FromUin, e)
                return
            
        action.sendFriendText(ctx.FromUin, str(msgDate))


            
    


if __name__ == '__main__':
    bot.run()