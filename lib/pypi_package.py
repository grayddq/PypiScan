# -*- coding: utf-8 -*-

import requests, os, tarfile, shutil, zipfile
from bs4 import BeautifulSoup
from scan_python import scan_python


class Pypi_Scan:
    def __init__(self, systempath):
        self.systempath = systempath
        # 文件目录和解压目录
        self.tmppath = systempath + "/tmp/"
        # 数据存放目录
        self.dbpath = systempath + "/db/pypi/"
        # 日志存放目录
        self.logpath = systempath + "/log/log.txt"
        # pypi网站地址
        self.PypiURL = "https://pypi.org"
        # pypi包路径
        self.PypiURLSimple = "https://pypi.org/simple/"

    # 获取pypi有多少项目，项目的名称和链接
    def pypi_packages_projects(self):
        packagesProjects = []
        response = requests.get(self.PypiURLSimple)
        if response.status_code != 200: return packagesProjects
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.find_all('a'):
            packagesProjects.append({"name": a.string, "url": self.PypiURL + a['href']})

        return packagesProjects

    def get_file_extension(self, filename):
        return filename.split(".")[-1]

    # 通过项目信息，获取项目安装文件和链接信息
    def get_packages_project_files(self, project):
        info = project
        response = requests.get(project["url"])
        if response.status_code != 200: return
        soup = BeautifulSoup(response.text, "html.parser")
        projectInfo = []
        for a in soup.find_all('a'):
            if self.get_file_extension(a.string) == "whl":
                projectInfo.append({"name": a.string, "url": a['href'], "type": "whl"})
            else:
                projectInfo.append({"name": a.string, "url": a['href'], "type": "tar"})

        info["versioninfo"] = projectInfo

        return info

    # 下载包文件
    def download_package_file(self, url_file, filename):
        try:
            r = requests.get(url_file, stream=True)
            f = open(filename, "wb")
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            return True
        except Exception as e:
            return False

    # 删除某目录下所有文件
    def del_file(self, tardir, filename):
        try:
            os.remove(filename)
            shutil.rmtree(tardir)
        except Exception as e:
            return False

    # 解压文件
    def untar(self, filename, path, type):
        try:
            if type == "whl":
                t = zipfile.ZipFile(filename)
            else:
                t = tarfile.open(filename)
            t.extractall(path=path)
            t.close()
            return True
        except Exception as e:
            return False

    # 拷贝恶意文件到指定留存目录
    def copyfile(self, projectname, filepath):
        try:
            path = self.dbpath + projectname
            if not os.path.exists(path):
                os.makedirs(path)
            shutil.copy(filepath, path)
        except Exception as e:
            print(e)
            return False

    # 扫描目录文件内容的安全性
    def scan_security(self, project, path):
        try:
            filepath = scan_python(self.systempath,path)
            if not filepath: return False
            self.copyfile(project, filepath)
            return True
        except Exception as e:
            return False

    # 扫描pypi包的安全性
    # 参数：项目名称、包地址、文件下载到本地文件路径、解压路径、包类型
    # 处理流程：
    # 1、下载安全包
    # 2、解压安全包
    # 3、扫描恶意内容
    # 4、存储恶意文件
    # 5、删除临时文件
    def scan_package(self, project, url, filename, tardir, type):
        security = False
        # 下载文件
        self.download_package_file(url, filename)
        # 解压文件
        if self.untar(filename, tardir, type):
            # 扫描文件内容
            if self.scan_security(project, tardir):
                security = True
        # 删除临时文件目录
        self.del_file(tardir, filename)
        return security


if __name__ == "__main__":
    # Pypi_Scan("/Users/grayddq/Grayddq/01.mygit/21.PypiScan/").scan_security("a","/Users/grayddq/Grayddq/01.mygit/21.PypiScan/tmp/libpeshnx-0.1")
    if Pypi_Scan("/Users/grayddq/Grayddq/01.mygit/21.PypiScan/").scan_package("0121",
                                                                              "https://files.pythonhosted.org/packages/99/b1/8329b44e81c794ebe8772531fbb94df3afb107102d183c1b0a17abb49471/0121-0.0.1.tar.gz#sha256=c340f511c652c50e67fac4e85528064f4253f5850446c9258949574a5d541f92",
                                                                              "/Users/grayddq/Grayddq/01.mygit/21.PypiScan/tmp/0121-0.0.1.tar.gz",
                                                                              "/Users/grayddq/Grayddq/01.mygit/21.PypiScan/tmp/0121/",
                                                                              "gz"):
        print("True")
