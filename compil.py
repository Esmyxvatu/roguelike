from cx_Freeze import setup, Executable

executables = [Executable("core/__main__.py")]

setup(
    name="Roguelike",
    version="1.0",
    description="Roguelike game",
    executables=executables
)