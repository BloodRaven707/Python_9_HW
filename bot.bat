@echo off

call %~dp0env\Scripts\activate

set BLOODRAVEN707BOTTOKEN=указать_здесь_токен_без_кавычек

python bot.py
:: inline_keys_in_bot.py
:: inline_bot.py

:: Выводиться не будут
REM Будет выводиться во время выполнения bat-файла, если нет @echo off

pause