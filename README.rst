哔哩哔哩直播间互动工具
======================

特色
-----

- 基于asyncio，可以满足更加丰富的使用场景
- 基于bilibili三代协议，支持brotli压缩算法，效率更高

安装
-----

::

    pip install bilibili-live


使用
-----

首先创建事件处理器类，类需要继承BilibiliLiveEventHandler类，并重写需要监听的事件方法：

::

    class MyEventHandler(BilibiliLiveEventHandler):
        def onDanmu(self, data: Danmu):
            # do something
            ...

具体支持的事件可以参考BilibiliLiveEventHandler类


完成后，创建BilibiliLive对象，并启动监听：

::

    room_id = 2411716
    # 此处房间号为短号，即用户直接可见的房间号
    bilibiliLive = BilibiliLive()
    bilibiliLive.schedule(MyEventHandler(), room_id)
    bilibiliLive.start()

需要退出时，可使用stop方法停止：

::

    bilibiliLive.stop()


此时即开启了事件循环。此函数为异步（非阻塞函数）。

本模块基于asyncio设计。start函数为一个包装函数，其中创建了一个线程并包装了协程操作。如需要直接使用asyncio方式操作，可使用start_asyncio函数。
