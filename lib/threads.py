# -*- coding: utf-8 -*-

import time, threading, Queue, sys, os
from consle_width import getTerminalSize
from pypi_package import *


class Threads_Scan:
    def __init__(self, thread=10, systempath=os.path.dirname(os.path.abspath(__file__))):
        # 线程数
        self.thread = thread
        # 系统目录
        self.system_path = systempath
        # 日志存放目录
        self.logpath = systempath + "/log/log.txt"
        # 文件目录和解压目录
        self.tmppath = systempath + "/tmp/"
        # 日志存储
        self.outfile = open(self.logpath, 'w')
        # 多线程框架
        self.thread_count = 0
        self.scan_count = self.found_count = 0
        self.lock = threading.Lock()
        self.console_width = getTerminalSize()[0] - 2
        self.msg_queue = Queue.Queue()
        self.STOP_ME = False
        threading.Thread(target=self._print_msg).start()
        self._init_queue()

    def _print_msg(self):
        while not self.STOP_ME:
            try:
                _msg = self.msg_queue.get(timeout=0.1)
            except:
                continue

            if _msg == 'status':
                msg = '%s Found| %s projects| %s scanned in %.1f seconds| %s threads' % (
                    self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time,
                    self.thread_count)
                sys.stdout.write('\r' + ' ' * (self.console_width - len(msg)) + msg)
            else:
                sys.stdout.write('\r' + _msg + ' ' * (self.console_width - len(_msg)) + '\n')
            sys.stdout.flush()

    def _update_scan_count(self):
        self.last_scanned = time.time()
        self.scan_count += 1

    def _update_found_count(self):
        self.found_count += 1

    # 获取项目信息，并加入队列中
    def _init_queue(self):
        self.msg_queue.put('[+] Initializing, get pypi package...')
        self.queue = Queue.Queue()

        project = Pypi_Scan(self.system_path).pypi_packages_projects()
        # 加入队列
        for info in project:
            self.queue.put(info)
        self.msg_queue.put('[+] Found pypi project %d in total' % len(project))

        self.outfile.write('[+] Found pypi project %d in total\n' % len(project))
        self.outfile.flush()

    # 开始多线程扫描
    def _scan(self):
        self.lock.acquire()
        self.thread_count += 1
        self.lock.release()

        pypiScan = Pypi_Scan(self.system_path)

        while not self.STOP_ME:
            try:
                lst_info = self.queue.get(timeout=0.1)
            except Queue.Empty:
                break

            while not self.STOP_ME:
                self._update_scan_count()
                self.msg_queue.put('status')

                # 获取project项目的包信息
                info = pypiScan.get_packages_project_files(lst_info)
                for t in info["versioninfo"]:
                    # 扫描项目中的包信息
                    # 项目名称、包地址、文件下载到本地文件路径、解压路径、包类型
                    if pypiScan.scan_package(info["name"], t["url"], self.tmppath + t["name"],
                                             self.tmppath + info["name"], t["type"]):
                        # 检测到恶意代码
                        self._update_found_count()
                        msg = ("Malicious project,project: %s, version: %s" % (info["name"], t["name"])).ljust(30)
                        self.msg_queue.put(msg)
                        self.msg_queue.put('status')
                        self.outfile.write(msg + '\n')
                        self.outfile.flush()
                        break
                break

        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()
        self.msg_queue.put('status')

    def run(self):
        self.msg_queue.put('[+] start scan projects ...')
        self.start_time = time.time()
        for i in range(self.thread):
            try:
                t = threading.Thread(target=self._scan, name=str(i))
                t.setDaemon(True)
                t.start()
            except:
                pass
        while self.thread_count > 0:
            try:
                time.sleep(1.0)
            except KeyboardInterrupt, e:
                msg = '[WARNING] User aborted, wait all slave threads to exit...'
                sys.stdout.write('\r' + msg + ' ' * (self.console_width - len(msg)) + '\n\r')
                sys.stdout.flush()
                self.STOP_ME = True
        self.STOP_ME = True
