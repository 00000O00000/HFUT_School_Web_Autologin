import tkinter as tk
import tkinter.messagebox as messagebox
import threading
import requests
import os

root = ''

def show_info_box():
    messagebox.showinfo("注意事项", "1、只有在\"待登录\"状态下初始化配置文件，用户IP、物理地址、用户网关才可以获得正确值。\n2、如果配置错误，删除config.cfg即可重新初始化。\n3、每次修改后，请点击保存按钮。\n4、本程序会在log文件夹下生成日志，一般情况下可定期清理。\n5、最后三个值非必要情况下请勿改动。\n6、密码不得有空格。")

# 配置文件模板，使用.format填充内容
cfg_m = """
# 账号基础配置
user_account = {}
user_password = {}

# 程序运行配置
runtime_delay = {}

# 网络信息配置
wlan_user_ip = {}
wlan_user_mac = {}
wlan_ac_ip = {}

# 高级链接参数
callback = {}
login_method = {}
v = {}
"""

def get_info():
    url = "http://www.msftconnecttest.com/redirect?cmd=redirect&arubalp=12345"          # 微软连接验证链接
    try:
        response = requests.get(url)            # 此处不可登录，否则会跳转至MSN，之后无法从链接中提取有效信息
    except:
        messagebox.showerror("错误", "当前未连接网络，请检查网络设置。")            # 未连接校网时报错
        quit()
        
    wlan_user_ip = ''
    wlan_user_mac = ''
    wlan_ac_ip = ''
    final_url = response.url            # 利用微软连接验证的跳转，获得完整的校网登录链接
    
    infos = final_url.split("&")        # 解析校网登录链接，提取必要信息
    for info in infos:
        if 'switchip' in info:
            wlan_ac_ip = info.split("=")[1]
            continue
        if 'mac' in info:
            wlan_user_mac = info.split("=")[1]
            continue
        if 'ip' in info:
            wlan_user_ip = info.split("=")[1]
            continue
    return wlan_user_ip, wlan_user_mac, wlan_ac_ip

def submit(entries):            # “提交”按钮的函数，将用户输入的内容保存至配置文件
    input_values = [entry.get() for entry in entries]
    cfg = cfg_m.format(input_values[0], input_values[1], input_values[2], input_values[3], input_values[4], input_values[5], input_values[6], input_values[7], input_values[8])
    with open("config.cfg", "w", encoding='utf-8') as file:
        file.write(cfg + "\n")
    
def create_gui(label_texts, input_values):
    # 提示信息盒
    infobox = threading.Thread(target=show_info_box)
    infobox.start()
    # 创建GUI界面
    root = tk.Tk()
    root.title("校园网自动登录系统")
    title_label = tk.Label(root, text="校园网自动登录配置", font=("Aria", 12))
    title_label.pack()
    frames = []
    for _ in range(10):
        frame = tk.Frame(root)
        frames.append(frame)
    labels = []
    for i in range(9):
        frame = frames[i]
        label = tk.Label(frame, text=label_texts[i])
        label.pack(side=tk.LEFT)
        labels.append(label)
    entries = []
    for i in range(9):
        frame = frames[i]
        entry = tk.Entry(frame)
        entry.insert(0, input_values[i])
        entry.pack(side=tk.LEFT)
        entries.append(entry)
    for i in range(6, 9):
        entries[i].config(state='disabled')         # 不推荐用户修改后三个内容，输入框设置为不可编辑
    frame = frames[9]
    submit_button = tk.Button(frame, text="   保存   ", command=lambda: submit(entries))
    submit_button.pack(anchor=tk.CENTER)
    for frame in frames:
        frame.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

def main():
    label_texts = ["校网账号", "校网密码", "运行延时", "用户IPv4", "物理地址", "用户网关", "回调模式", "登录模式", "版本编号"]
    input_values = []
    if os.path.exists("config.cfg"):        # 存在config时，软件直接读取config文件，然后展示
        with open("config.cfg", "r", encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if '=' in line:
                    input_values.append(line.split("=")[1].strip())
    else:           # 不存在config时，软件尝试获取必要内容，然后展示
        input_values = ["YourAccount", "YourPassword", "1","Local IPv4", "Local MAC", "Local Gateway", "dr1003", "8", "5835"]
        input_values[3:6] = get_info()
    create_gui(label_texts, input_values)

if __name__ == '__main__':
    main()