# -*- coding: utf-8 -*-

# 作者：咚咚呛
# 版本：v0.1
# 功能：本程序旨在为扫描整个pypi库的恶意代码特征，包含：后门类、挖矿类、勒索类、信息盗取类等

from lib.threads import *
import optparse

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--thread", dest="thread", type="int", default=10, help=u"线程数")

    options, _ = parser.parse_args()

    pypi = Threads_Scan(thread=options.thread, systempath=os.path.dirname(os.path.abspath(__file__)))
    pypi.run()
    pypi.outfile.flush()
    pypi.outfile.close()
