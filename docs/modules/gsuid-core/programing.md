---
title: 编写插件
description: 服务
sidebar_position: 1
---
## 插件示例

***需要进一步修改***

```python
import asyncio

from gsuid_core.sv import SL, SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event


@SV('开关').on_prefix(('关闭', '开启')) # 定义一组服务`开关`，服务内有两个前缀触发器
async def get_switch_msg(bot: Bot, ev: Event):
    name = ev.text         # 获取消息除了命令之外的文字
    command = ev.command   # 获取消息中的命令部分
    im = await process(name)  # 自己的业务逻辑
    await bot.logger.info('正在进行[关闭/开启开关]')  # 发送loger
    await bot.send(im)   # 发送消息

sv=SV(
    name='复杂的服务',  # 定义一组服务`开关`,
    pm=2, # 权限 0为master，1为superuser，2为群的群主&管理员，3为普通
    priority=5, # 整组服务的优先级
    enabled=True, # 是否启用
    black_list=[] # 黑名单
)

@sv.on_prefix('测试')
async def get_msg(bot: Bot, ev: Event):
    ...
```