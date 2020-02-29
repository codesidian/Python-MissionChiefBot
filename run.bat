@ECHO OFF
date /t
echo - MISSION CHIEF BOT 16/02/2020-
echo - Creative Commons Attribution-NonCommercial 4.0 International License -
echo - Copyright 2020 Jack Bayliss / Joshua Latham license available - https://github.com/codesidian/Python-MissionChiefBot/blob/master/LICENSE.md -
echo checking for new requirements
cd botfiles
pip install -r requirements.txt
py missionchief_bot.py && python3 missionchief_bot.py

if %errorlevel% == 0 (
  echo Oh something seemed to crash, maybe post an issue.. We'll try re-running!
  py missionchief_bot.py && python3 missionchief_bot.py
)