___
A new version of this bot has been released which you can find [here](https://github.com/jackbayliss/Mission-Chief-Bot)
That however means we'll be focusing more on the newer version, which is around 400% quicker. Although any **MAJOR** bugs will still be supported on this version. If you're planning to run on either MACOS or Linux I would use this version rather than the newer version for now.
___


![Build Status](https://github.com/codesidian/Python-MissionChiefBot/workflows/Mission%20Chief%20Tests/badge.svg)
# The Free Mission Chief Bot

A bot written to automate the grinding and boring jobs of the bot, simply follow the guide and let it run. No fee to pay, no license required. 

**The bot uses chromedriver in order to emulate the user, this helps with going undetected so please ensure you have Chrome installed.**
## Features
- Open source, no hidden viruses.
- Automatic despatching.
- Ability to read missions requirements.
- Practically undetectable, using only user avaiable buttons and pages- no API calls all using the browser.
- Hide the browser from opening - set `headless_mode` to `true` in your config.ini.
- Send only a batch of missions at a time - set `mission_batch_amount` to the amount required in your config.ini.
- Super fast, the bot caches any vehciles and mission it comes across.
- Multiple domains supported, .co.uk, .com, .ru.
- Multiple accounts at one time, just create another bot in another folder and off you go.
- Debug logging built in.


## How to use
Download the code [here](https://github.com/codesidian/Python-MissionChiefBot/archive/master.zip), make sure you install Python from [here](https://www.python.org/downloads/) then extract the files to a folder of your choice (Just keep the files together)

Once done open the `config.ini` inside the config folder and replace corresponding `email` and `password` with your account information, and `server` with the country  your account is registered on such as `uk`. All working countries will be in the `server.ini`
`mission_batch_amount` is the amount of missions it will do per batch, so if it finds 100 missions. It will do the set amount.
If you don't want to see the browser window set `headless_mode` to `true`.
If you need the bot to transport patients etc, please set `run_despatcher` to `true`.


### Windows
Once you're done double click the `run.bat` located in the main folder. This will force check any requirements and run the script for you. 

### Linux
 cd into the bots directory and run `bat run.sh`. This will force check any requirements and run the script for you. Ensure python is installed.
 
 ### Mac
 cd into the bots directory and run `bat run.sh`. This will force check any requirements and run the script for you. Ensure python is installed.

## Increase speed
If you'd like to increase the speed of the bot, I would recommend running `generatemissions.bat` or run `generate.py` (located in the botfiles folder) before running the bot, this will cache/save all the missions it can find with requirements ready for the bot to read.

## How to run the bot for 24 hours a day, without relying on your own computer
If you're interested in how to run this bot all day, for as little as $5 a month please follow the following guide:
[https://github.com/jackbayliss/MissionChiefBot-linux](https://github.com/jackbayliss/MissionChiefBot-linux)

## Issues / Bugs / Errors

If you have any issues and would like to let us know directly, please join our discord.
<p align="center">
  <a href="https://discord.gg/fxKtSuD">
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
