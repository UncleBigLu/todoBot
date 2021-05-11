import re

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

# m = re_time.match(test_list[0])
# print(m.group(7))

