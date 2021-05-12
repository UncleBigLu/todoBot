from botoy import Action, Botoy, GroupMsg
from botoy import decorators as deco
import os

from myRegex import parse_input
from sqlFunc import insert_data

bot = Botoy()
masterQQ = os.environ['targetQQ']

def mark_event():
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
    if insert_data(parse_ret[0], parse_ret[1]) == False:
        action.sendFriendText(ctx.FromUin, "数据库故障了Σ(っ °Д °;)っ")
    



            
    


if __name__ == '__main__':
    bot.run()