import pygame
from com.base.singleton import Singleton


class Sounds(Singleton):
    music_playing = False
    current_music = None

    url = ""

    def __single__(self):
        pygame.init()
        pygame.mixer.init()

        self.music_playing = False
        self.current_music = None

    def play_music(self, music_file, loop=-1):
        """
        播放音乐
        :param music_file: 音乐文件路径
        :param loop: 循环次数，-1表示无限循环，0表示不循环，1表示循环1次
        """
        if self.music_playing:
            self.stop_music()

        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(loop)
        self.music_playing = True
        self.current_music = music_file

    def stop_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
            self.current_music = None

    def get_current_music(self):
        return self.current_music

    def verify_playing(self, b: bool = True):
        if len(self.url) < 3:
            return

        if b:
            if not Sounds().music_playing:
                # 使用loop=1表示播放1次（即总共播放1遍）
                Sounds().play_music(self.url, loop=-1)
        else:
            if Sounds().music_playing:
                Sounds().stop_music()

    def reset_music(self):
        """重置音乐状态，允许重新播放"""
        self.music_playing = False
        self.current_music = None
