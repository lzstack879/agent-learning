import asyncio

async def task1():
    print('hello')
    await asyncio.sleep(1)  # 暂停 1 秒，把控制权交还给事件循环
    print('world')

async def task2():
    print('foo')
    await asyncio.sleep(2)
    print('bar')

async def main():
    # 并发运行两个任务，等它们都完成
    await asyncio.gather(
        task1(),
        task2(),
    )

asyncio.run(main())