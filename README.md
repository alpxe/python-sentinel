## 软件说明 python-sentinel

梦幻西游,网络错误提示工具. 支持手机提醒

### 基础功能:

检测到“网络错误” 就会开始放提示音乐  
可以自定义自己喜欢的mp3音乐

### 其他功能:

1) 填写自己游戏的ID,子窗口闪退也会提示  
   (该功能,只支持存在一个大窗口的情况下)
2) 填写手机号,飞书机器人会发送消息通知  
   (需要下载飞书APP)

当然,不填也不会影响基础功能

### 测试方法

可以创建一个记事本,  
命名成"网络错误",  
打开它 进行模拟测试.

也可以自己把号顶了,创建一个网络错误

### 关于 手机收到消息通知

访问[飞书官网](https://www.feishu.cn/download),下载APP,并用手机注册账号.

加我进组织,就可以了

<img src="./card.jpg" alt="飞书二维码" width="220">


最后效果如下:  
<img src="./renderings.jpg" alt="效果图" width="220">

### 打包指令

```
pyinstaller --onefile --windowed --add-data="bgm.mp3;." --name sentinel main.py
pyinstaller --clean sentinel.spec
```
