# 哔哩哔哩直播间互动工具

[![Author](https://img.shields.io/badge/Author-Gedoy-red.svg "Author")](https://github.com/Gedoy9793 "Author")
[![LICENSE](https://img.shields.io/badge/license-MIT-green.svg "LICENSE")](./LICENSE "LICENSE")
[![python](https://img.shields.io/badge/python-3.7|3.8|3.9|3.10-blue.svg "Python")](https://www.python.org/ "Python")


## 特色

- 基于asyncio，可以满足更加丰富的使用场景
- 基于bilibili三代协议，支持brotli压缩算法，效率更高
- 事件钩子部分使用泛型，开发更友好

## 安装

``` bash
pip install bilibili-live
```

## 使用

首先创建事件处理器类，类需要继承BilibiliLiveEventHandler类，并重写需要监听的事件方法：

``` python
from bilibili_live.events import BilibiliLiveEventHandler, Danmu, Event

class MyEventHandler(BilibiliLiveEventHandler):
    def onDanmu(self, event: Event[Danmu]):
        # do something
        ...
```

> 具体支持的事件可以参考BilibiliLiveEventHandler类


完成后，创建BilibiliLive对象，并启动监听：

``` python
from bilibili_live import BilibiliLive

room_id = 2411716
# 此处房间号为短号，即用户直接可见的房间号
bilibiliLive = BilibiliLive()
bilibiliLive.schedule(MyEventHandler(), room_id)
bilibiliLive.start()
```

需要退出时，可使用stop方法停止：

``` python
bilibiliLive.stop()
```

此时即开启了事件循环。此函数为异步（非阻塞函数）。

本模块基于asyncio设计。start函数为一个包装函数，其中创建了一个线程并包装了协程操作。如需要直接使用asyncio方式操作，可使用start_asyncio函数。
