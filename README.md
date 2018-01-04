# A web crewler for pixiv

## 依赖

* python 2.7
* requests

## 代理

因为GFW，爬P站需自备梯子，默认代理为：

```
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080"
}
```

可以按照个人情况修改`pixiv.py`的11-14行。

## usage

不指定图片id，则爬国际排行榜

```
python pixiv.py -e your-email -p your-password
```

指定图片id，则爬指定图片

```
python pixiv.py -e your-email -p your-password -i img-id
```

`your-email`和`your-password`是你的P站账号的邮箱和密码