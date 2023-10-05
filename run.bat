@echo off
pip install virtualenv
virtualenv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
call venv\Scripts\deactivate.bat
