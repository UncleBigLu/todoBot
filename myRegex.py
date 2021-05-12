import re
from datetime import datetime, timedelta

# test_list = [
#     '提醒 今天下午14点干一件事',
#     '提醒 3月29日1点干啥',
#     '提醒 5点干啥'
# ]

pattern = r'^提醒\s((今天|明天|后天|大后天)|((20\d{2}年)?(1?\d月)?([1-3]?\d日?)))?(上午|下午)?([1-2]?\d点)?'
re_time = re.compile(pattern)

# group2: 今天 明天 后天 大后天
# group3: 年月日
# group4: 年
# group5: 月
# group6: 日
# group7: 上午 下午
# group8: 点

def parse_input(ctx, action):
    m = re_time.match(ctx.Content)
    currentTime = datetime.now()
    msgDate = None  # Year, month, day
    msgTime = None # minute, 
    if(m!=None):
        if(m.group(2) != None and m.group(3) != None):
            action.sendFriendText(ctx.FromUin, "不能同时出现日期和今天明天啦！")
            return None
        
        if(m.group(2) == None and m.group(3) == None):
            msgDate = currentTime
        if(m.group(2) != None and m.group(3) == None):
            if(m.group(2) == "今天"):
                msgDate = currentTime
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
            else:
                month = currentTime.month
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
                action.sendFriendText(ctx.FromUin, str(e))
                return None

        if(m.group(7) == None and group(8) == None):
            msgTime = datetime(2000, 1, 1, 20)
        elif(m.group(8) == None):
            if(m.group(7) == "上午"):
                msgTime = datetime(2000, 1, 1, 12)
            else:
                msgTime = datetime(2000, 1, 1, 20)
        elif(m.group(7) == None):
            tmp = int(m.group(7)[:-1])
            try:
                msgTime = datetime(2000, 1, 1, tmp)
            except ValueError as e:
                action.sendFriendText(ctx.FromUin, str(e))
                return None
        else:
            tmp = int(m.group(8)[:-1])
            if(m.group(7) == "上午"):
                if(tmp > 12):
                    action.sendFriendText(ctx.FromUin, "上午怎么可能超过12点嘛！")
                    return None
                msgTime = datetime(2000, 1, 1, tmp)
            else:
                if(tmp < 12):
                    msgTime = datetime(2000, 1, 1, tmp+12)
                else:
                    try:
                        msgTime = datetime(2000, 1, 1, tmp)
                    except ValueError as e:
                        action.sendFriendText(ctx.FromUin, str(e))
                        return None
        msgDate = msgDate.replace(hour=msgTime.hour, minute=0, second=0, microsecond=0)
        if msgDate < currentTime:
            action.sendFriendText(ctx.FromUin, "时间已经过了啦...")
            return None
        
        # Get the event name
        time_len = len(m.group(0))
        event_name = ctx.Content[time_len:]
        return [msgDate, event_name]
