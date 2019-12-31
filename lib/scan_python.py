# -*- coding: utf-8 -*-

import os, sys


def load_rule(systempath):
    rules = []
    for root, dirs, files in os.walk(systempath + "/lib/rule"):
        for filespath in files:
            if filespath[-3:] == '.py':
                rulename = filespath[:-3]
                if rulename == '__init__':
                    continue
                __import__('lib.rule.' + rulename)
                rules.append(rulename)
    return rules


def scan_python(systempath, path):
    rules = load_rule(systempath)
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.split(".")[-1] != 'py': continue
            filepath = os.path.join(root, filename)
            if os.path.getsize(filepath) < 500000:
                for rule in rules:
                    file = open(filepath, "rb")
                    filestr = file.read()
                    file.close()
                    if sys.modules['lib.rule.' + rule].Check(filestr,filename):
                        return filepath
    return ""


if __name__ == "__main__":
    print scan_python("/Users/grayddq/Grayddq/01.mygit/21.PypiScan/test/libpeshnx-0.1")
