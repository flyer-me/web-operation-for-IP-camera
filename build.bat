@echo off
for %%i in (main.py) do ( pyinstaller --version-file info.txt -F "%%i" && rmdir /s /q build )
for /r %%i in ("dist\*.exe") do move /Y "%%i" .\
rd /s /q "dist"
del *.spec