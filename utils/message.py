from colorama import Fore, Style

class PrintMessage:
    def __init__(self):
        pass

    def debug(self, msg):
        print(f'''{Fore.YELLOW}~~~~~~~~~~ DEBUG ~~~~~~~~~~
{msg}
~~~~~~~~~~ DEBUG ~~~~~~~~~~{Style.RESET_ALL}''')

    def info(self, msg):
        print(f'''{Fore.CYAN}~~~~~~~~~~ INFO ~~~~~~~~~~
{msg}
~~~~~~~~~~ INFO ~~~~~~~~~~{Style.RESET_ALL}''')

    def ok(self, msg):
        print(f'''{Fore.GREEN}~~~~~~~~~~ OK ~~~~~~~~~~
{msg}
~~~~~~~~~~ OK ~~~~~~~~~~{Style.RESET_ALL}''')

    def error(self, msg):
        print(f'''{Fore.MAGENTA}~~~~~~~~~~ ERROR ~~~~~~~~~~
{msg}
~~~~~~~~~~ ERROR ~~~~~~~~~~{Style.RESET_ALL}''')

