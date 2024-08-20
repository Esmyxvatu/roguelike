from datetime import datetime
import pygame as pg
import psutil
import time


def get_ram_usage() -> float:
    process = psutil.Process()
    mem_info = process.memory_info()
    ram_usage_mb = mem_info.rss / (1024**2)  # Convertir les bytes en MB
    ram_usage_mb = round(ram_usage_mb, 3)
    return ram_usage_mb


def get_cpu_usage() -> float:
    cpu_usage = psutil.cpu_percent()
    return cpu_usage


def set_caption(clock: pg.time.Clock, last_update_time:float, update_interval: float = 0.25) -> float:
    if time.time() - last_update_time > update_interval:
        pg.display.set_caption(f"Roguelike - FPS: {int(clock.get_fps())} - {get_ram_usage()}MB RAM - {get_cpu_usage()}% CPU")
        return time.time()
    else :
        return last_update_time


class Logger:
    def __init__(self, filename: str, processus: str) -> None:
        self.file = filename
        self.proc = processus

    def write(self, message: str, date: datetime) -> None:
        # on parse la date
        date = date.strftime("%Y-%m-%d %H:%M:%S.%f")
        message = f"{date}{message}"

        with open(self.file, "a") as f:
            f.write(message)

    def info(self, message: str) -> None:
        msg = f" [i] {self.proc} : {message}\n"
        date = datetime.now()
        self.write(msg, date)

    def error(self, message: str) -> None:
        msg = f" [e] {self.proc} : {message}\n"
        date = datetime.now()
        self.write(msg, date)

    def warning(self, message: str) -> None:
        msg = f" [w] {self.proc} : {message}\n"
        date = datetime.now()
        self.write(msg, date)
