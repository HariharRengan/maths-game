@echo off
call venv\Scripts\activate.bat
pip install flask
python app.py
call venv\Scripts\deactivate.bat