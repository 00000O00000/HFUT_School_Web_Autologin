# 自动登录校园网脚本
<img src="https://www.hfut.edu.cn/images/xh_logo.png" width="20%" height="auto">

该项目是一个用于合肥工业大学学生，自动登录校园网的Python脚本。

在初次配置完成后，它可以自动完成校园网登录操作，省去每次开机都需要手动登录的烦恼。

## 相关要求
作者是屯溪路校区的学生，对于翡翠湖校区的校网情况并不清楚，请翡翠湖校区的同学按需修改代码。

* 操作系统：Windows 7/10/11

* python版本要求： python 3

## 原理

作者通过抓包，获取到了校园网登录接口（此为屯溪路登录接口，翡翠湖未知，请自行抓包）

接口请求为GET方式，其中共有8个参数，通过配置生成器获取并保存。您也可以自行通过这个接口，开发属于自己的校园网自动登录脚本。

```python
url = "http://210.45.240.105:801/eportal/?c=Portal&a=login&callback={}&login_method={}&user_account={}&user_password={}&wlan_user_ip={}&wlan_user_ipv6=&wlan_user_mac={}&wlan_ac_ip={}&wlan_ac_name=&jsVersion=3.3.2&v={}"
```


## 预编译文件运行
如果你嫌麻烦，不用担心！

向右看，“release”里，“预编译exe软件包”，开箱即用！

请按照以下流程操作

### ①下载文件

下载右侧“预编译exe软件包”内的第一个压缩包，然后解压到本地；

### ②运行配置程序

第一次启动此程序时，需配置自动登录。一次配置后，之后无需再进行配置。

请在连接了校网，但没有登录的情况下，运行“自动登录配置生成器.exe”。

### ③填充信息

请根据自己的实际情况，填写1、2、3行内容。

如果你在正确的时机运行了此程序，那么4、5、6行会自动填充正确信息。若这3行为空白，请重启此程序。

填写完成后，点击保存，然后关闭此程序


### ④设置开机自启动

请按照如下步骤操作

* 复制软件本体，“校园网自动登录.exe”；

* 在桌面右键，点击“粘贴快捷方式”，根据自己喜好重命名该快捷方式；

* 复制如下地址，打开文件资源管理器，在上方地址栏粘贴；
```plaintext
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
```
* 将桌面刚刚粘贴的快捷方式，拖到这个文件夹里。

### 注意事项

* 【重要】如果您需要使用此脚本，请在“设置” - “网络和Internet” - “WLAN”中，关闭“随机硬件地址”选项；

* 部分杀毒软件会拦截未知的开机启动项，请在对应杀毒软件的设置页同意此程序的开机自启权限；

* 请根据实际情况，调整脚本配置内的“延时”选项，确保程序运行成功的同时不会影响使用体验。

* 如果发现脚本登录失败，请删除config.cfg，然后重新按照步骤②，运行“自动登录配置生成器.exe”

### 至此，该程序的配置已全部完成。在这之后，软件将自动为您登录校网。


## 源代码运行
在你开始使用该脚本之前，请确保已正确安装Python环境。你可以从Python官方网站（https://www.python.org）下载并安装最新版本的Python。

### ①下载、安装
将本项目下载到本地，然后进入项目目录，并安装所需的依赖：
```plaintext
pip install requests
```
### ②运行配置脚本
在首次运行此项目时，先启动配置文件生成器。

请在连接了校网，但没有登录的情况下，启动该脚本！该脚本仅在此条件下，可以正常获得所需的配置信息。
```plaintext
python config_generator.py
```
如果您在正确的时机运行了该脚本，那么出现的窗口中，第4、5、6行会自动填充正确的值。

### ③填充信息

请在第1、2行填入校网登录信息，然后在第三行填入登录延时（s）。这用于应对，电脑还未连接校网，脚本就执行登录操作，导致的登录失败情况。

检查信息无误，然后点击保存，这时完整的配置信息会存放在同目录，供主程序读取。


### ④运行登录脚本
在上述操作完成后，您便完成了此脚步的配置流程。请使用如下命令启动登录脚本。
```plaintext
python auto_login.py
```
脚本将自动读取配置文件，并完成校园网登录过程。如果一切顺利，您不会收到任何弹窗。

## 【强烈推荐】编译脚本为exe
如果你希望将脚本编译为可运行的exe文件，可以使用PyInstaller工具。PyInstaller将脚本及其依赖打包成一个独立的可执行文件，方便在不安装Python解释器的情况下运行。

首先，确保已经全局安装了PyInstaller：

```plaintext
pip install pyinstaller
```

然后，在项目根目录中执行以下命令：
```plaintext
pyinstaller --onefile --noconsole auto_login.py
pyinstaller --onefile --noconsole config_generetor.py
```

执行完毕后，将会生成一个dist目录，在其中可以找到编译后的可执行文件。

可执行文件的便携程度很高，您可以将生成的exe文件直接与其他人分享，他们可以直接双击运行，无需安装Python解释器或任何依赖。


--------------
希望这个脚本对你有所帮助！如果你有任何问题或建议，请随时提出。谢谢！

与我联系：

E-mail : 1528518618@qq.com

QQ : 1528518618
