@ECHO OFF
date /t
echo - MISSION CHIEF BOT 10/03/2020-
echo - Creative Commons Attribution-NonCommercial 4.0 International License -
echo - Copyright 2020 Jack Bayliss / Joshua Latham license available - https://github.com/codesidian/Python-MissionChiefBot/blob/master/LICENSE.md -
echo checking for new requirements
cd scripts
py get-pip.py && python3 get-pip.py && python get-pip.py
cd ../botfiles
pip install -r requirements.txt
py generate.py && python3 generate.py  && python generate.py

if %errorlevel% == 0 (
  echo Oh something seemed to crash, maybe post an issue.. We'll try re-running!
  py missionchief_bot.py && python3 missionchief_bot.py
)
pause