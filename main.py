import os
from datetime import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import sys

from com.capitals.binding import Binding
from com.capitals.pusher import Pusher
from com.capitals.sounds import Sounds
from com.view.page import Ui_Dialog


class MainForm(QMainWindow, Ui_Dialog):
    timer = None

    music = ""  # 音乐文件夹

    pid = None
    hwnd = None  # 大窗口

    count = 0

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        try:
            # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
            base_path = sys._MEIPASS
        except Exception:
            # 开发环境使用当前目录
            base_path = os.path.abspath(".")

        self.music = os.path.join(base_path, "bgm.mp3")

        self.init_ui()
        self.init_event()

    def init_ui(self):
        self.hwnd = Binding().leadership()

        Sounds().url = self.music
        self.musicTxt.setText(os.path.basename(self.music))

        self.pid = self.lineEdit.text().strip()
        pass

    def init_event(self):
        self.lineEdit.textChanged.connect(self.__text_changed_handler)
        self.phoneEdit.textChanged.connect(self.__phone_changed_handler)
        self.musicBtn.clicked.connect(self.__music_click_handler)

        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__update)  # 连接更新函数
        self.timer.start(1000)  # 每秒触发一次（1000毫秒）

    def __text_changed_handler(self, e):
        text = e.strip()
        if text:
            self.pid = text
        else:
            # 如果输入全是空格，可以给出提示
            if e and not text:
                print("当前只输入了空格")

    def __phone_changed_handler(self, e):
        text = e.strip()
        if text:
            Pusher().phone = text
        else:
            # 如果输入全是空格，可以给出提示
            if e and not text:
                print("当前只输入了空格")

    def __music_click_handler(self):
        # 打开文件选择器
        file_path, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口
            "选择音乐文件",  # 对话框标题
            "",  # 默认目录
            "音频文件 (*.mp3);"  # 文件过滤器
        )

        if file_path:  # 如果用户选择了文件（没有取消）
            self.music = file_path

            Sounds().url = self.music
            self.musicTxt.setText(os.path.basename(self.music))
        else:
            print("用户取消了选择")

    def __judge(self):
        """最终判断 0:无情况  1:网络错误  2:子号闪退"""
        playing = False  # 判断子号是否存在
        multiple = False
        if self.hwnd > 0 and not Binding().minimized():
            if self.pid and len(self.pid) > 3:
                multiple = True
                if Binding().has_pid(self.pid):
                    playing = False  # 号还在
                else:
                    playing = True  # 号不在

        if multiple and playing:
            return 2
        else:
            return 0 if Binding().network() else 1

    def __update(self):
        flag = self.__judge()
        if flag == 0:
            Sounds().verify_playing(False)
            self.count = 0
        else:
            Sounds().verify_playing(True)
            tips = "网络错误" if flag == 1 else "游戏闪退"
            tips += f"  {datetime.now().strftime('%Y-%m-%d,%H:%M:%S')}"

            if self.count == 0:
                Pusher().send_msg(tips)

            self.count += 1
            self.count %= 10


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()

    sys.exit(app.exec_())
