from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from com.base.singleton import Singleton
import os


class Sounds(Singleton):
    _player = None
    url = ""
    _should_be_playing = False  # 逻辑开关，标记用户是否想要播放

    def __single__(self):
        self._player = QMediaPlayer()
        # 监听状态改变
        self._player.stateChanged.connect(self.__handle_state_changed)

    def __handle_state_changed(self, state):
        # 只有当【播放自然结束】且【逻辑上仍需要播放】时，才触发重播
        if state == QMediaPlayer.StoppedState and self._should_be_playing:
            self._player.play()

    def play_music(self):
        if not os.path.exists(self.url):
            return

        # 检查当前设置的媒体是否已经是该文件，避免重复加载导致的“卡顿”
        file_url = QUrl.fromLocalFile(os.path.abspath(self.url))
        content = QMediaContent(file_url)

        # 只有路径变了才重新 setMedia，否则直接 play
        if self._player.media().canonicalUrl() != file_url:
            self._player.setMedia(content)

        self._player.play()

    def verify_playing(self, b: bool = True):
        # 更新逻辑开关
        self._should_be_playing = b

        if len(self.url) < 3:
            return

        if b:
            # 如果没在播，就让它播
            if self._player.state() != QMediaPlayer.PlayingState:
                self.play_music()
        else:
            # 如果正在播，就停掉
            if self._player.state() == QMediaPlayer.PlayingState:
                self._player.stop()