from os import name
import sqlite3
import time


class Record_row:
    def __init__(
        self,
        id: int,
        stu: str,
        last_time: float,
        next_time: float,
        stat: int,
        name: str
    ) -> None:
        self.id = id
        self.stu = stu
        self.last_time = last_time
        self.next_time = next_time
        self.stat = stat
        self.name = name


def get_last_records(path: str):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT *
    FROM record JOIN name ON record.stu = name.stu
    GROUP BY record.stu
    HAVING last = MAX(last);
    ''')
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    now = time.localtime(time.time())
    today = time.mktime(time.struct_time((
        now.tm_year,
        now.tm_mon,
        now.tm_mday,
        0, 0, 0,
        now.tm_wday,
        now.tm_yday,
        now.tm_isdst
    )))
    records = []
    for each in result:
        records.append(Record_row(each[0], each[1], each[2], each[3], each[4], each[6]))
        if int(each[2]) < today:
            records[len(records) - 1].stat = -114
    return records

async def construct_msg(path):
    records = get_last_records(path)
    msg_list = []
    msg_list.append('🔔 报平安情况 🔔')
    msg_list.append('统计时间：{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    for each in records:
        if each.stat == 0:
            stat_str = '🟢 成功'
        elif each.stat == -1:
            stat_str = '🟡 成功（之前已报）'
        elif each.stat == -114:
            stat_str = '🔴 失败（无数据，请检查后端服务）'
        else:
            stat_str = '🔴 失败'
        last_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(each.last_time))
        next_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(each.next_time))
        msg_list.append('''{} 同学：
报平安状态：{}
上次执行时间：{}
下次预估执行时间：{}\n'''.format(
            each.name if each.name else each.stu,
            stat_str,
            last_time_str,
            next_time_str
        ))
    msg_list.append('⚠️ 如有突发情况 请在预估执行时间之前自行报平安')
    return f'\n'.join(msg_list)
