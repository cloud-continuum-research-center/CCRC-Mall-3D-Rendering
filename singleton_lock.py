# deprecated

class LogLock:
    is_lock = 0
    instance = None
    
    def __new__(cls, *args, **kwargs):
        if LogLock.instance is None:
            LogLock.instance = super().__new__(cls)
        return LogLock.instance
    
    def __init__(self):
        self.is_lock = 1
    
    @staticmethod
    def get_instance():
        if not LogLock.instance:
            raise ValueError('first __init__')
        else:
            return LogLock.instance
    
    
    def lock(self):
        self.is_lock = 1
    def unlock(self):
        self.is_lock = 0
    
    def lock_state(self):
        print(self.is_lock)
        return self.is_lock