# Python Mission Chief Bot

A small bot for the game missionchief written in Python

**This bot is meant for use with standard Chrome, please do not use any MissionChief mods, such as LSS manager as it may affect the bot.**

## Features
- Open source, no hidden viruses.
- Automatic despatching.
- Ability to read missions requirements.
- Practically undetectable, using only user avaiable buttons and pages- no API calls.
- Hide the browser from opening - set `headless_mode` to `true` in your config.ini.
- Send only a batch of missions at a time - set `mission_batch_amount` to the amount required in your config.ini.
- Super fast, the bot caches any vehciles and mission it comes across.
- Multiple domains supported, .co.uk, .com, .ru.
- Multiple accounts at one time, just create another bot in another folder and off you go.
- Debug logging built in.


## How to use
Download the code [here](https://github.com/codesidian/Python-MissionChiefBot/archive/master.zip), make sure you install Python from [here](https://www.python.org/downloads/) then extract the files to a folder of your choice (Just keep the files together)

Once done open the `config.ini` and replace corresponding `email` and `password` with your account information, and `url` with the domain your account is registered on such as `https://www.missionchief.co.uk/`. 
`mission_batch_amount` is the amount of missions it will do per batch, so if it finds 100 missions. It will do the set amount.
If you don't want to see the browser window set `headless_mode` to `true`

### Windows
Once you're done double click the `run.bat` located in the main folder. This will force check any requirements and run the script for you. 

### Linux
 `cd` into the botfiles folder, download the requirements with `pip install -r requirements.txt` and run either `python missionchief_bot.py` or `py missionchief_bot.py` depending on your python version
 
 ### Mac
 `cd` into the botfiles folder, download the requirements with `pip install -r requirements.txt` and run either `python missionchief_bot.py` or `py missionchief_bot.py` depending on your python version


## Issues / Bugs / Errors

If you have any issues and would like to let us know directly, please join our discord.
<p align="center">
  <a href="https://discord.gg/DshUEeg">
    <img src="https://discordapp.com/api/guilds/676191159638425620/widget.png?style=banner2" />
  </a>
</p>

If you have any issues please create an issue [here](https://github.com/codesidian/Python-MissionChiefBot/issues)


## Contributing

If you'd like to contribute please feel free to make a fork, which will then be reviewed.


## License
This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License
see license [here](https://github.com/codesidian/Python-MissionChiefBot/blob/master/LICENSE.md)

## Disclaimer
Section 7.2 of the MissionChief official rules state:
`Use of tools, scripts, bots or other computer programs:Users are not allowed to use tools, scripts, bots or other computer programs which are suitable for the automatic execution of actions in a game.`

No developers of this bot hold any responsability for your use of it. We make no warranties about the effectiveness, or performance of this bot. If you're banned, that's on you. 

**USE AT YOUR OWN RISK**
