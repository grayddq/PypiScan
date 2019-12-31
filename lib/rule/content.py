# -*- coding: utf-8 -*-


# 解码类
# rule1
encry_keywords = ["base64.b64decode("]

# rule2
# 网络传输类
net_keywords = ["socket.socket",
                "urllib.request",
                "urllib.urlopen",
                "urllib2.urlopen",
                "requests.get",
                "requests.post"
                ]

# rule3
# 命令执行类
exec_keywords = ["os.system",
                 "os.popen",
                 "commands.getstatusoutput",
                 "commands.getoutput",
                 "commands.getstatus",
                 "os.chmod",
                 " exec("
                 ]

# rule4
# 本地敏感文件
local_keywords = [".bashrc",
                  "/.ssh/id_rsa"
                  ]

# rule5
# 敏感特征
malice_keywords = ["exec(base64.b64decode("]


# 规则，符合如下
# rule2 + rule1
# rule2 + rule3
# rule2 + rule4
# rule5


def Check(filestr,filename):
    filestr = filestr.lower()
    rule1, rule2, rule3, rule4, rule5 = False, False, False, False, False

    if filename == "setup.py":
        if "base64.b64decode(" in filestr:
            return True

    for key in encry_keywords:
        if key in filestr:
            rule1 = True
    for key in net_keywords:
        if key in filestr:
            rule2 = True
    for key in exec_keywords:
        if key in filestr:
            rule3 = True
    for key in local_keywords:
        if key in filestr:
            rule4 = True
    for key in malice_keywords:
        if key in filestr:
            rule5 = True

    if rule1 & rule2:
        return True
    elif rule1 & rule3:
        return True
    elif rule2 & rule3:
        return True
    elif rule2 & rule4:
        return True
    elif rule5:
        return True
    else:
        return False
