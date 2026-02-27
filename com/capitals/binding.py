import re
from xmlrpc.client import Boolean
import win32gui

from com.base.singleton import Singleton


class Binding(Singleton):
    dm = None

    leader = 0  # 主线大窗口句柄
    size = [0, 0]  # 主线大窗口 width,height

    roles = []

    @staticmethod
    def __windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            windows.append((hwnd, title))

    @staticmethod
    def __children_callback(hwnd, windows):
        # 获取窗口的类名和标题
        window_title = win32gui.GetWindowText(hwnd)
        window_class = win32gui.GetClassName(hwnd)

        if window_class == "WSGAME":
            match = re.search(r"梦幻西游 ONLINE - \(.+ - (.+)\[(\d+)]", window_title)
            if match:
                windows.append((hwnd, match.group(1), match.group(2)))

    def __single__(self):
        pass

    def leadership(self, XYQ_TITLE=r"梦幻西游 ONLINE"):
        """
        大窗口
        """
        windows = []
        win32gui.EnumWindows(self.__windows_callback, windows)
        for hwnd, title in windows:
            if len(title) > 0 and re.search(XYQ_TITLE, title):
                self.leader = hwnd
                print("主窗口句柄:", self.leader)

                self.__masses(hwnd)
                break

        return self.leader

    def __masses(self, leader: int):
        """
        管理与维护该窗口句柄下的子窗口
        """
        windows = []
        win32gui.EnumChildWindows(leader, self.__children_callback, windows)

        self.roles = [{"hwnd": hwnd, "name": name, "pid": pid} for hwnd, name, pid in windows]

    def has_pid(self, pid):
        for index, obj in enumerate(self.roles):
            if obj["pid"] == pid:
                return True

        # 更新子窗口,再次查找
        self.__masses(self.leader)
        for index, obj in enumerate(self.roles):
            if obj["pid"] == pid:
                return True

        return False

    def active(self):
        """
        大窗口是否置顶
        """
        return win32gui.GetForegroundWindow() == self.leader

    def minimized(self):
        """
        大窗口是否最小化
        """
        return Boolean(win32gui.IsIconic(self.leader))

    def network(self):
        """
        运行活力
        @return False:网络错误
        """
        windows = []
        win32gui.EnumWindows(self.__windows_callback, windows)
        for hwnd, title in windows:
            if "网络错误" in title:
                return False
        return True
