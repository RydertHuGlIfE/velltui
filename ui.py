import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

a= r'____   ____     .__  ._________________ ___.___ '
b= r'\   \ /   /____ |  | |  \__    ___/    |   \   |'
c= r' \   Y   // __ \|  | |  | |    |  |    |   /   |'
d= r'  \     /\  ___/|  |_|  |_|    |  |    |  /|   |'
e= r'   \___/  \___  >____/____/____|  |______/ |___|'
f= r'              \/                                '

def print_ban():
        lines = [a,b,c,d,e,f]
        for i, lines in enumerate(lines):
                print(colors[i%len(colors)] + lines )
