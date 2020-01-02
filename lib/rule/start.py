# -*- coding: utf-8 -*-


# 启动项类
start_keywords = ["Software\Microsoft\Windows\CurrentVersion\Run"]


def Check(filestr, filename):
    filestr = filestr.lower()

    for key in start_keywords:
        if key in filestr:
            return True

    return False
