from botoy import Action, Botoy, GroupMsg
from botoy import decorators as deco
import os
from apscheduler.schedulers.background import BackgroundScheduler
import psycopg2

from myRegex import parse_input
from sqlFunc import insert_data, select_daily, select_per_hour

bot = Botoy()
masterQQ = os.environ['targetQQ']
botQQ = os.environ['botQQ']
action = Action(botQQ)

def mark_event():
    # Mark_event as done
    # TO DO
    return


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
    if ctx.MsgType == "ReplayMsg":
        # Mark the event as completed
        mark_event()
        return

    # Try to add new event
    parse_ret = parse_input(ctx, action)
    if parse_ret is None:
        return
    # action.sendFriendText(ctx.FromUin, str(parse_ret[0])+'\n'+str(parse_ret[1]))
    # Insert data to SQL
    try:
        insert_data(parse_ret[0], parse_ret[1])
    except psycopg2.DatabaseError:
        action.sendFriendText(ctx.FromUin, "数据库故障了Σ(っ °Д °;)っ")
  
    rmsg = "任务收到!\n" + str(parse_ret[0]) + "\n" + parse_ret[1]
    action.sendFriendText(ctx.FromUin, rmsg)
    

def daily_remind():
    msg = "早安喵~今日日程安排在这里啦："
    try:
        s = select_daily()
    except psycopg2.DatabaseError:
        action.sendFriendText(ctx.FromUin, "数据库故障了Σ(っ °Д °;)っ")
 
    
    for i in s:
        msg += '\n' + i[0]
    action.sendFriendText(int(masterQQ), msg)


def remind_per_hour():
    msg = "还有很多工作没有做，还不能休息喔："
    try:
        s = select_per_hour()
    except psycopg2.DatabaseError:
        action.sendFriendText(ctx.FromUin, "数据库故障了Σ(っ °Д °;)っ")
    if len(s) == 0:
        return
    for i in s:
        msg += '\n' + i[0] + '\n' + str(i[1])
    action.sendFriendText(int(masterQQ), msg)
            

if __name__ == '__main__':
    scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Shanghai'})
    scheduler.add_job(daily_remind, 'cron', hour=7, minute=59)
    scheduler.add_job(remind_per_hour, 'cron', minute=59)
    scheduler.start()
    bot.run()