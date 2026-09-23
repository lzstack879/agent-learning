# 写3个模拟 I/O 函数，对比顺序 await 与并发执行耗时

import asyncio
import time

TASKS = [("任务A", 1.0), ("任务B", 2.0), ("任务C", 1.5)]

def blocking_io(name: str, delay: float) -> str:
    """阻塞式 I/O：time.sleep 会占住线程"""
    print(f"  [{name}] 开始，耗时 {delay}s")
    time.sleep(delay)
    print(f"  [{name}] 完成")
    return name

def run_sequential():
    """顺序执行（同步阻塞，一个一个做）"""
    start = time.perf_counter()
    for name, delay in TASKS:
        blocking_io(name, delay)
    return time.perf_counter() - start

async def async_io(name: str, delay: float) -> str:
    """异步 I/O：await 时释放事件循环"""
    print(f"  [{name}] 开始，耗时 {delay}s")
    await asyncio.sleep(delay)
    print(f"  [{name}] 完成")
    return name

async def run_async_sequential():
    """情况 2：顺序 await（无并发，一次只等一个）"""
    start = time.perf_counter()
    for name, delay in TASKS:
        await async_io(name, delay)
    return time.perf_counter() - start

async def run_async_concurrent() -> float:
    """情况 3：并发执行（gather 同时启动）"""
    start = time.perf_counter()
    await asyncio.gather(*(async_io(name, delay) for name, delay in TASKS))
    return time.perf_counter() - start

async def main():
    print("=" * 45)
    print("情况 1：顺序执行（同步阻塞）")
    print("=" * 45)
    t1 = run_sequential()
    print(f"耗时: {t1:.2f}s\n")

    print("=" * 45)
    print("情况 2：异步执行（顺序 await，无并发）")
    print("=" * 45)
    t2 = await run_async_sequential()
    print(f"耗时: {t2:.2f}s\n")

    print("=" * 45)
    print("情况 3：异步执行（gather 并发）")
    print("=" * 45)
    t3 = await run_async_concurrent()
    print(f"耗时: {t3:.2f}s\n")


if __name__ == "__main__":
    asyncio.run(main())