import requests
import prettytable
import datetime
import stdiomask

from shutil import get_terminal_size

from termcolor import colored

DISCORD_API_URL = 'https://discord.com/api/v9'
BOT_TOKEN = 'MTEwNzIxMDM3MDU2MjY2MjQ5MA.G0M4X7.GhotMEq2g6WpaxgYnK0pyJBWnYRvUYAckb9bQo'

def print_centered_text(text):
    terminal_width = get_terminal_size().columns
    colors = ['red', 'light_red']  # Different shades of purple
    for i, line in enumerate(text.splitlines()):
        print(colored(line.center(terminal_width), colors[i%len(colors)]))

def run():
    user_id = stdiomask.getpass(prompt=colored('[?] User ID: ', 'white'), mask='*')
    user_info = get_user_info(user_id)
    if user_info:
        display_user_info(user_info)
    else:
        print_centered_text(colored(f'Could not find user with ID: {user_id}', 'white'))

def get_user_info(user_id):
    headers = {'Authorization': f'Bot {BOT_TOKEN}'}
    response = requests.get(f'{DISCORD_API_URL}/users/{user_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_user_info(user_info):
    table = prettytable.PrettyTable()
    table.field_names = ['Field', 'Value']
    table.align = 'l'

    table.add_row(['ID', user_info['id']])
    table.add_row(['Username', f"{user_info['username']}#{user_info['discriminator']}"])
    table.add_row(['Avatar', user_info['avatar']])
    table.add_row(['Bot', user_info['bot'] if 'bot' in user_info else 'False'])
    table.add_row(['System', user_info['system'] if 'system' in user_info else 'False'])
    table.add_row(['MFA Enabled', user_info['mfa_enabled'] if 'mfa_enabled' in user_info else 'False'])

    print_centered_text('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print_centered_text("\nUser Information:\n")
    print_centered_text(str(table))
    print_centered_text('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

    input(colored("\nPress Enter to return to the main menu.\n", 'white'))
