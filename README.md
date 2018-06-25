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

可以按照个人情况修改`pixiv.py`的14-17行。

## usage

不指定图片id，则爬国际排行榜

```
python pixiv.py -e your-email -p your-password
```

`-i`指定图片id，则爬指定图片

```
python pixiv.py -e your-email -p your-password -i img-id
```

`-k`指定关键词，可以搜索相关图片并按照like数排序下载，可以用-c指定下载前几张(默认前10张，最多前400张)

```
python pixiv.py -e your-email -p your-password -k "fate 5000"
python pixiv.py -e your-email -p your-password -k "fate 5000" -c 20
```

关键词后面加上数字(1000、5000、10000、20000等)可以筛选出like数大于等于这个数字的图片

`your-email`和`your-password`是你的P站账号的邮箱和密码

