@echo off
set PYTHONIOENCODING=utf-8
set dc_path="%~d0\%~p0descarga-cfdi"
py %dc_path% %*
