@echo off 
manage.py makemigrations 
if not 0 == %errorlevel% goto error 
manage.py migrate 
if not 0 == %errorlevel% goto error 
start manage.py runserver 
goto end 
:error 
pause 
:end 
