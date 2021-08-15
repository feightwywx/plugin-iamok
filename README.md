# plugin-iamok

[haust-iamok](https://github.com/feightwywx/iamok)的配套[nonebot2](https://github.com/nonebot/nonebot2)插件

## 使用方式

进行配置并加载插件即可

私聊/群聊提到机器人并说“报平安情况”即可获取报平安情况，自动报平安在进行配置后会自动运行

## 配置项

### iamok_sqlite_path

`hause-iamok`建立的sqlite3数据库文件路径

### iamok_report_time_hr

报告时间的小时数，默认值`12`

### iamok_report_time_min

报告时间的分钟数，默认值`0`

（也就是默认每天中午12:00发送）

### iamok_msg_type

消息类型，支持`private`或者`group`，默认值`private`

### iamok_id

如果消息类型为`private`就填QQ号，如果为`group`就填群号
