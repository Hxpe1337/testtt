import json
import stdiomask
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import pyfiglet
from colorama import init, Fore

console = Console()

def print_title(text):
    ascii_art = pyfiglet.figlet_format(text)
    console.print(Text(ascii_art, style="bold cyan"))

def run():
    # Load settings
    try:
        with open('settings.json', 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = {}

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

        print_title("Settings Menu")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option Number", justify="center")
        table.add_column("Setting", justify="left")
        table.add_row("1", "Set Discord Webhook")
        table.add_row("2", "Set Bitcoin Address")
        table.add_row("3", "Set User ID")
        table.add_row("4", "View Current Settings")
        table.add_row("5", "Exit to Main Menu")

        console.print(table)

        choice = console.input(Text("Choose an option: ", style="bold yellow"))

        if choice == '1':
            settings['discord_webhook'] = stdiomask.getpass(prompt='Enter Discord Webhook URL: ', mask='*')
        elif choice == '2':
            settings['bitcoin_address'] = stdiomask.getpass(prompt='Enter Bitcoin Address: ', mask='*')
        elif choice == '3':
            user_id = input('Enter User ID (without <@ and >): ')
            settings['user_id'] = f"<@{user_id}>"
        elif choice == '4':
            console.print(Panel(Text("Current Settings", style="bold cyan"), expand=False))
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Setting", justify="left")
            table.add_column("Value", justify="left")
            for key, value in settings.items():
                table.add_row(f"{key}", f"{value}")
            console.print(table)
            console.input(Text("\nPress Enter to return to the Settings Menu.\n", style="bold yellow"))
        elif choice == '5':
            break
        else:
            console.print(Text("Invalid choice, please try again.", style="bold red"))

        # Save settings
        with open('settings.json', 'w') as file:
            json.dump(settings, file, indent=4)

        console.print(Panel(Text("Settings saved successfully.", style="bold green"), expand=False))

    console.print(Panel(Text("Returning to the main menu...", style="bold cyan"), expand=False))

if __name__ == "__main__":
    init(autoreset=True)  # Initialize colorama
    run()
