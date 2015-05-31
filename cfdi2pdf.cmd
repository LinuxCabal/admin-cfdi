@echo off
set PYTHONIOENCODING=utf-8
set c2p_path="%~d0\%~p0cfdi2pdf"
py %c2p_path% %*
