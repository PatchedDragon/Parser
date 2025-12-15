
from colorama import Fore, Style, init
init(autoreset=True)

def banner():
    logo = f"""{Fore.RED}
    ██████╗  █████╗ ██████╗ ███████╗██████╗ 
    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██████╔╝███████║██████╔╝█████╗  ██████╔╝
    ██╔═══╝ ██╔══██║██╔══██╗██╔══╝  ██╔══██╗
    ██║     ██║  ██║██║  ██║███████╗██║  ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """

    info = f"""
    {Fore.CYAN}Creator{Style.DIM}: ALI Raza
    {Fore.CYAN}Github{Style.DIM}: https://github.com/PatchedDragon/Pasrser
    {Fore.CYAN}Status{Style.DIM}: Under Development
    """

    print(logo + info)

banner()