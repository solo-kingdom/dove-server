# coding: utf-8
import imghdr
import os
import urllib.request
from uuid import uuid4

from spider.public.utils import generate_random_str_id


def download_pic(url, save_path):
    # 下载图片
    _res = urllib.request.urlopen(url)
    print('下载图片:', _res.status)
    _pic_content = _res.read()
    # 获取图片格式
    _pic_suffix = imghdr.what('', h=_pic_content)
    # 生成随机图片名
    _pic_name = str(uuid4()) + '.' + _pic_suffix
    # 包含名称保存路径
    _pic_save_path_with_name = os.path.join(save_path, _pic_name)
    # 如果路径不存在, 则创建
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # 保存
    with open(_pic_save_path_with_name, 'wb') as f:
        f.write(_pic_content)
    # 返回图片名称
    print('下载图片:', _pic_save_path_with_name)
    return _pic_name

if __name__ == "__main__":
    print(download_pic('https://img3.doubanio.com/lpic/s29437536.jpg', './a/b/c'))
