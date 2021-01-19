# coding: utf-8
# 工具类
import os.path
import pathlib
import re


def get_file_name(file_path):
    """给出文件路径, 返回带有后缀的文件名"""
    file_path = str(file_path).strip()
    return os.path.split(file_path)[-1]


def get_file_name_without_suffix(file_path):
    """给出文件路径, 返回不带后缀的文件名"""
    file_path = str(file_path).strip()
    return os.path.split(file_path)[-1].split('.')[0]


def get_specific_file_list(dir_path=None, suffix=None, recursion=False):
    """
    获取目录下特定后缀文件
    :param dir_path: 目录路径
    :param suffix: 后缀, str或者list
    :param recursion: 是否递归搜索子文件夹
    :return: 文件列表
    """
    _res = []
    try:
        if dir_path is None or suffix is None or not os.path.exists(dir_path):
            return _res
        for item in os.listdir(dir_path):
            item = os.path.join(dir_path, item)

            # 如果是文件
            if os.path.isfile(item):
                # 如果后缀是字符串
                if isinstance(suffix, str) and is_specific_suffix(item, suffix):
                    _res.append(os.path.join(dir_path, item))
                # 如果后缀是列表
                elif isinstance(suffix, list):
                    for _suffix in suffix:
                        if is_specific_suffix(item, _suffix):
                            _res.append(os.path.join(dir_path, item))
            elif os.path.isdir(item) and recursion:
                # 如果是路径且递归查找
                _recursion_res = get_specific_file_list(os.path.join(dir_path, item), suffix, recursion=recursion)

                for _t_res in _recursion_res:
                    _res.append(_t_res)
    except:
        # import traceback
        # traceback.print_exc()
        return _res
    return _res


def is_specific_suffix(file_path, suffix):
    """
    判断给定文件是否是特定后缀
    :param file_path: 
    :param suffix: 
    :return: 
    """
    suffix = str(suffix).lower()
    suffix = suffix if suffix.startswith('.') else '.' + suffix
    if pathlib.PurePath(file_path).suffix.lower() == suffix:
        return True
    return False


if __name__ == '__main__':
    # print(is_specific_suffix('/home/a.mp3', '.mp3'))
    # print(is_specific_suffix('/home/a.mp3', 'mp3'))
    # print(is_specific_suffix('/home/a.mp3', 'Mp3'))
    pass
    # print(is_specific_suffix('/home/a.mp3', 'Mp4'))
