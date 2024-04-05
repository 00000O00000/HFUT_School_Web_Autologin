import requests
import os
import time
import datetime
from tkinter import messagebox

# 校网自动登录接口
urlTemplate = 'http://210.45.240.105:801/eportal/?c=Portal&a=login&callback={}&login_method={}&user_account={}&user_password={}&wlan_user_ip={}&wlan_user_ipv6=&wlan_user_mac={}&wlan_ac_ip={}&wlan_ac_name=&jsVersion=3.3.2&v={}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/105'
}

# 一个简易的日志系统
class mylogs:
    def __init__(self, head):
        if not os.path.exists("./log"):
            os.makedirs("log")
        now = datetime.datetime.now()
        self.filepath = 'log\\'
        self.filename = "login-log-" + now.strftime("%Y-%m%d-%H%M%S") + ".log"
        with open(self.filepath + self.filename, "a") as file:
            file.write(f"当前时间: {datetime.datetime.now()}\n")
            file.write(f"{head}\n以下是日志信息:\n\n")
    def a_log(self, info, msg):
        now = datetime.datetime.now()
        log_text = f"{now} | {info} | {msg}"
        with open(self.filepath + self.filename, "a") as file:
            file.write(log_text + "\n")
        print(log_text)
logs = mylogs("校园网自动登录日志")

# 读取配置文件，返回字典
def read_config(filepath = '.\\'):
    config = {}
    try:
        with open(filepath + "config.cfg", "r", encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if '=' in line:
                    key, value = line.split("=")
                    key = key.strip()
                    value = value.strip()
                    config.setdefault(key, value)
    except FileNotFoundError:
        logs.a_log("INFO", "用户配置文件'config.cfg'未找到，请先运行配置文件生成器。\n程序运行结束。按任意键退出. . .")
        messagebox.showerror("自动登录失败", "用户配置文件'config.cfg'未找到，请先运行配置文件生成器。")
        quit()
    return config

def main():
    logs.a_log("INFO", "欢迎使用 合肥工业大学 校园网自动登录软件")
    
    # 以下读取配置信息
    config = read_config()
    config['wlan_user_mac'] = "".join([c.lower() for c in config['wlan_user_mac'] if c != "-"])             # 将mac地址转化为合法形式
    url = urlTemplate.format(config['callback'], config['login_method'], config['user_account'], config['user_password'], config['wlan_user_ip'], config['wlan_user_mac'], config['wlan_ac_ip'], config['v'])
    logs.a_log("INFO", "当前配置信息：")
    for key,value in config.items():
        logs.a_log("INFO", "{} : {}".format(key, value))
    logs.a_log("INFO", "自动登录将在{}秒后开始。".format(config['runtime_delay']))
    time.sleep(int(config['runtime_delay']))
    logs.a_log("INFO", "开始自动登录。\n=========================")
    
    # 以下发送登录请求
    try:
        response = requests.get(url, headers=headers)           # 发送登录请求
    except Exception as e:          # requests直接报错，通常是没有连接校网/没联网导致的
        logs.a_log("ERROR", e)
        logs.a_log("ERROR", "自动登录失败，网络未连接！")
        messagebox.showerror("自动登录失败", "自动登录失败，网络未连接！")
        quit()
        
    # 以下通过接口返回内容，验证是否登录成功
    if response.status_code == 200:
        if '"result":"1"' in response.text:         # 接口返回内容验证，result=1则为登录成功，否则为失败
            logs.a_log("INFO", "自动登录成功。")
        else:
            logs.a_log("INFO", "自动登录失败，请重试或检查参数！")
            logs.a_log("INFO", "请求链接：{}\n返回参数：{}".format(url, response.text))
            messagebox.showerror("自动登录失败", "自动登录失败，请重试或检查参数！\n请求链接：{}\n返回参数：{}".format(url, response.text))
    else:       # 校网服务器出现异常时报错
        logs.a_log("INFO", '请求失败:', response.status_code)
    logs.a_log("INFO", "程序运行结束。")
    
if __name__ == '__main__':
    main()
