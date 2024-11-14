@echo off
pyinstaller --noconsole --add-data "Config.yml;." --icon=Icon\Icon.ico --onefile GenshinStoryClicker.py
pause