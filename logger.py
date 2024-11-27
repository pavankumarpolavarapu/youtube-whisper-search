from __future__ import annotations


class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl,
        # both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        if 'Extracting' in msg:
            print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
