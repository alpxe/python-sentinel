import threading


class Singleton(object):
    """
    单例模式超类
    __single__ 仅执行一次
    """

    _lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        if hasattr(cls, "_instance"):
            return cls._instance

        with cls._lock:
            if not hasattr(cls, "_instance"):
                cls._instance = object.__new__(cls)
                cls._instance.__single__(*args, **kwargs)

        return cls._instance

    def __single__(self, *args):
        """ only init once """
        pass
