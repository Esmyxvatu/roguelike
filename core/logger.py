from datetime import datetime

class Logger:
    def __init__(self, filename, processus):
        self.file = filename
        self.proc = processus

    def write(self, message, date):
        # on parse la date
        date = date.strftime("%Y-%m-%d %H:%M:%S.%f")
        message = f"{date}{message}"

        with open(self.file, "a") as f:
            f.write(message)

    def info(self, message):
        msg = f" [i] {self.proc} : {message}\n"
        date = datetime.now()
        self.write(msg, date)

    def error(self, message):
        msg = f" [e] {self.proc} : {message}\n"
        date = datetime.now()
        self.write(msg, date)

    def warning(self, message):
        msg = f" [w] {self.proc} : {message}\n"
        date = datetime.now()
        self.write(msg, date)
