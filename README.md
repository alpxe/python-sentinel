## 软件说明 python-sentinel

### 基础功能:

检测到“网络错误” 就会开始放提示音乐  
可以自定义自己喜欢的mp3音乐

### 其他功能:

1) 填写自己游戏的ID,子窗口闪退也会提示
2) 填写手机号,飞书机器人会发送消息通知

不填也不会影响基础功能

### 测试方法

可以创建一个记事本,  
命名成"网络错误",  
打开它 进行模拟测试.

### 关于 手机收到消息通知

访问[飞书官网](https://www.feishu.cn/download),下载APP,并用手机注册账号.

加我进组织,就可以了
![](./card.jpg)

最后效果如下:
![](./renderings.jpg)

### 打包指令

```
pyinstaller --onefile --windowed --add-data="bgm.mp3;." --name sentinel main.py
pyinstaller --clean sentinel.spec
```
