import random,time
from colorama import init,Fore,Style

def randomsleep():
    sleepint= random.randint(1, 30)
    print(Fore.CYAN + f"Sleeping for {sleepint} seconds"+Style.RESET_ALL)

    time.sleep(sleepint)