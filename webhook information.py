import requests
import prettytable
import datetime
import stdiomask

from shutil import get_terminal_size

from termcolor import colored
def print_centered_text(text):
    terminal_width = get_terminal_size().columns
    colors = ['red', 'light_red']  # Different shades of purple
    for i, line in enumerate(text.splitlines()):
        print(colored(line.center(terminal_width), colors[i%len(colors)]))
def run():
    webhook = stdiomask.getpass(prompt=colored('[?] Webhook url: ', 'white'), mask='*')
    try:
        response = requests.get(webhook)
        response.raise_for_status()  # raise an exception if the response contains an HTTP error status code
        webhook_info = response.json()
        display_webhook_info(webhook_info)
    except requests.exceptions.HTTPError as err:
        print(f'HTTP error occurred: {err}')  # handle HTTP errors
    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')  # handle other request errors

def display_webhook_info(webhook_info):
    table = prettytable.PrettyTable()
    table.field_names = ['Field', 'Value']
    table.align = 'l'  # Set alignment of all columns to left

    table.add_row(['ID', webhook_info['id']])
    table.add_row(['Type', webhook_info['type']])
    table.add_row(['Guild ID', webhook_info['guild_id']])
    table.add_row(['Channel ID', webhook_info['channel_id']])
    table.add_row(['User ID', webhook_info['user']['id']])
    table.add_row(['User Name', f"{webhook_info['user']['username']}#{webhook_info['user']['discriminator']}"])
    table.add_row(['Name', webhook_info['name']])
    table.add_row(['Avatar', webhook_info['avatar']])
    table.add_row(['Token', webhook_info['token']])
    table.add_row(['Application ID', webhook_info['application_id']])

    created_at = datetime.datetime.fromtimestamp(((int(webhook_info['id']) >> 22) + 1420070400000) / 1000)
    table.add_row(['Created At', created_at])

    print_centered_text('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print_centered_text("\nWebhook Information:\n")
    print_centered_text(str(table))
    print_centered_text('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

    input(colored("\nPress Enter to return to the main menu.\n", 'white'))
