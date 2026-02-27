import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)



colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]


a= r'  _____________________________________ .____     ____ ___.___ '
b= r' /   _____/\_   ___ \______   \_   ___ \|    |   |    |   \   |'
c= r' \_____  \ /    \  \/|     ___/    \  \/|    |   |    |   /   |'
d= r' /        \\     \___|    |   \     \___|    |___|    |  /|   |'
e=r'/_______  / \______  /____|    \______  /_______ \______/ |___|'
f= r'        \/         \/                 \/        \/              '


def print_ban():
        lines = [a,b,c,d,e,f]
        for i, lines in enumerate(lines):
                print(colors[i%len(colors)] + lines )
