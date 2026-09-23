import asyncio

event_loop = asyncio.new_event_loop()

async def task1():
    print('hello')
    await asyncio.sleep(1)  # 暂停 1 秒，把控制权交还给事件循环
    print('world')

async def task2():
    print('foo')
    await asyncio.sleep(2)
    print('bar')

event_loop.create_task(task1())
event_loop.create_task(task2())

# 创建一个事件循环并无限循环地执行其作业集合
event_loop.run_forever()
