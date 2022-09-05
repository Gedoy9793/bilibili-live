哔哩哔哩直播间互动工具
======================

特色
-----

- 基于asyncio，可以满足更加丰富的使用场景
- 基于bilibili三代协议，支持brotli压缩算法，效率更高

安装
-----

(暂未发布)

::

    pip install bilibili-live


使用
-----

首先创建事件处理器类，类需要继承BilibiliDanmuEventHandler类，并重写需要监听的事件方法：

::

    class MyEventHandler(BilibiliDanmuEventHandler):
        def onDanmu(self, data: Danmu):
            # do something
            ...

当前支持的事件列表如下：

========== ============= ========
事件       方法名         参数类型
========== ============= ========
弹幕       onDanmu        Danmu
礼物       onGift         Gift
银瓜子礼物  onSilverGift   Gift
金瓜子礼物  onGoldGift     Gift
========== ============= ========


完成后，创建Observer对象，并启动监听：

::

    room_id = 2411716
    # 此处房间号为短号，即用户直接可见的房间号
    observer = Observer()
    observer.schedule(MyEventHandler(), room_id)
    observer.start()


此时即开启了事件循环。此函数为异步（非阻塞函数）。

本模块基于asyncio设计，start函数为一个包装函数，其中实际启用了一个事件循环。如需要直接使用asyncio方式操作，可使用start_asyncio函数。