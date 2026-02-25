### 软件说明 python-sentinel

检测到有: 网络错误 就会开始循环播放音乐  
(可以创建一个记事本命名成"网络错误",打开测试)

功能1: 可以换一个自己喜欢的mp3音乐  
基础功能,开启即用 

功能2: 填写自己游戏的ID,如果闪退了也会放歌  
不填 就会忽略这个功能2的逻辑,不影响功能1


```
pyinstaller --onefile --windowed --add-data="bgm.mp3;." --name sentinel main.py
pyinstaller --clean sentinel.spec
```

后续开发:  
添加邮箱提示  
需要提供 邮箱授权码,发送者邮箱,接收者邮箱  
目前担心增加软件使用成本  
