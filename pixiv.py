# -*- coding: utf-8 -*-
__author__ = 'f1sh'

import requests
import re
import os
import threading
import argparse
import time
from cStringIO import StringIO
from PIL import Image

s = requests.session()
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080"
}
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
}
get = []

#登录P站
def login(email, password):
    r = s.get("https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index", proxies = proxies)
    pattern = re.compile('<input type="hidden" name="post_key" value="(.*?)">', re.S)
    post_key = re.search(pattern, r.content).group(1)
    data = {
        "pixiv_id": email,
        "password": password,
        "captcha": "",
        "g_recaptcha_response": "",
        "post_key": post_key,
        "source": "pc",
        "ref": "wwwtop_accounts_index",
        "return_to": "https://www.pixiv.net/"
    }
    s.post("https://accounts.pixiv.net/api/login?lang=zh", data = data, headers = header, proxies = proxies)

#获取图片pid
def getPids():
    url = 'https://www.pixiv.net/ranking_area.php?type=detail&no=6'
    page = s.get(url, headers = header, proxies = proxies).content
    pattern = re.compile('<a href="member_illust\.php\?mode=medium&amp;illust_id=(.*?)">', re.S)
    pids = re.findall(pattern, page)
    return pids

#爬取图片
def getImg(pid):
    try:
        global get
        mediumUrl = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pid
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Referer": mediumUrl
        }
        r = s.get(mediumUrl, headers = header, proxies = proxies, stream = True)
        pattern = re.compile('"original":"(.*?)"', re.S)
        imgPath = re.search(pattern, r.content).group(1).replace('\\', '')
        if pid not in get:
            r = s.get(imgPath, headers = header, proxies = proxies)
            filename = 'pixiv/' + imgPath.split('/')[-1]
            img = Image.open(StringIO(r.content))
            img.save(filename)
            get.append(imgPath.split('/')[-1])
            print "[+] " + imgPath.split('/')[-1] + " saved."
        i = 1
        imgPath = imgPath.replace('p0', 'p' + str(i))
        r = s.get(imgPath, headers = header, proxies = proxies)
        while r.status_code == 200:
            if imgPath.split('/')[-1] not in get:
                filename = 'pixiv/' + imgPath.split('/')[-1]
                img = Image.open(StringIO(r.content))
                img.save(filename)
                get.append(imgPath.split('/')[-1])
                print "[+] " + imgPath.split('/')[-1] + " saved."
                i += 1
                imgPath = imgPath.replace('p' + str(i - 1), 'p' + str(i))
                r = s.get(imgPath, headers = header, proxies = proxies)
            else:
                i += 1
                imgPath = imgPath.replace('p' + str(i - 1), 'p' + str(i))
                r = s.get(imgPath, headers = header, proxies = proxies)
    except:
        getImg(pid)

#创建目录
def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    else:
        return False

# 获取列表的第二个元素
def takeSecond(elem):
    return elem[1]

#搜索图片
def search(keyword, count):
    pattern = re.compile('<input type="hidden"id="js-mount-point-search-result-list"data-items="(.*?)"', re.S)
    data = ''
    for i in xrange(1, 11):
        searchUrl = 'https://www.pixiv.net/search.php'
        params = {'s_mode': 's_tag', 'word': keyword, 'p': str(i)}
        r = s.get(searchUrl, params = params, headers = header, proxies = proxies)
        data += re.search(pattern, r.content).group(1)
    pattern = re.compile("&quot;illustId&quot;:&quot;(.*?)&quot;,.*?&quot;bookmarkCount&quot;:(.*?),", re.S)
    imgList = re.finditer(pattern, data)
    imgDatas = []
    for img in imgList:
        imgData = (img.group(1), int(img.group(2)))
        imgDatas.append(imgData)
    imgDatas.sort(key = takeSecond, reverse = True)
    pids = []
    ts = []
    count = count if count <= len(imgDatas) else len(imgDatas)
    for i in xrange(count if count <= 400 else 400):
        pids.append(imgDatas[i][0])
    for pid in pids:
        t = threading.Thread(target = getImg, args = (pid, ))
        ts.append(t)
        t.start()
    for t in ts:
        t.join()

#主函数
def main():
    start = time.time()
    ts = []
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", type = str)
    parser.add_argument("-p", "--password", type = str)
    parser.add_argument("-i", "--id", type = str ,nargs = "?", default = "")
    parser.add_argument("-k", "--key", type = str ,nargs = "?", default = "")
    parser.add_argument("-c", "--count", type = int ,nargs = "?", default = 10)
    arg = parser.parse_args()
    login(arg.email, arg.password)
    mkdir('pixiv')
    if arg.id != "":
        getImg(arg.id)
    elif arg.key != "":
        search(arg.key, arg.count)
    else:
        pids = getPids()
        for pid in pids:
            t = threading.Thread(target = getImg, args = (pid, ))
            ts.append(t)
            t.start()
        for t in ts:
            t.join()
    print "[*] Time cost: " + str(time.time() - start) + "s"

if __name__ == '__main__':
    main()