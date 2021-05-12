from botoy import Action, Botoy, GroupMsg
from botoy import decorators as deco
import os

from myRegex import parse_input

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

    msgDate = parse_input(ctx, action)
    if msgDate is None:
        return
    action.sendFriendText(ctx.FromUin, str(msgDate))


            
    


if __name__ == '__main__':
    bot.run()