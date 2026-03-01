import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

a= r'  __________  ___________________ ____ ___ .___ '
b= r'  \______   \/   _____/\__    ___/    |   \|   |'
c= r'   |       _/\_____  \   |    |  |    |   /|   |'
d= r'   |    |   \/        \  |    |  |    |  / |   |'
e= r'   |____|_  /_______  /  |____|  |______/  |___|'
f= r'          \/        \/                             '

def print_ban():
        lines = [a,b,c,d,e,f]
        for i, lines in enumerate(lines):
                print(colors[i%len(colors)] + lines )
