import sys

from cx_Freeze import setup, Executable

includefiles = ["option.ui", "tomor.ui", "conf.ini", "sound/bell.wav", "sound/school_bell.wav", "img/app.ico", "img/app.png",
                "img/pause.png", "img/play.png", "img/reset.png", "img/setting.png", "img/skip.png", "img/pomo_32.png"]
build_exe_options = {"packages": ["os", "pygubu"],
                     "excludes": ["PyQt4.QtCore", "PyQt4.QtGui"],
                     "include_files": includefiles,
                     "optimize": 2}
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable('domor.py', base=base, compress=True, icon='img/app.ico')
]

setup(name="Domor",
      version="0.1",
      description="A simple Pomodoro app",
      options={"build_exe": build_exe_options},
      executables=executables)
