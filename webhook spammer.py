from termcolor import colored
import requests
import time
import threading
import stdiomask
from shutil import get_terminal_size
import ctypes

stop_spamming = False
def print_centered_text(text):
    terminal_width = get_terminal_size().columns
    colors = ['red', 'light_red']  # Different shades of purple
    for i, line in enumerate(text.splitlines()):
        print(colored(line.center(terminal_width), colors[i%len(colors)]))


def spam(webhook, message, delay):
    global stop_spamming, messages_sent
    print_centered_text('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    while not stop_spamming:
        try:
            response = requests.post(webhook, json={'content': message})
            if response.status_code == 429:
                print_centered_text(colored(f'[429] Rate limit exceeded, waiting for 2 seconds', 'red'))
                time.sleep(2)  # wait for 2 seconds
            else:
                print_centered_text(f'[{response.status_code}] Succesfully sent message with content "{message}"')
                messages_sent += 1  # increment the counter
                ctypes.windll.kernel32.SetConsoleTitleW(f"to end the spammer click ENTER | messages sent: {messages_sent}")
            time.sleep(delay)
        except Exception as e:
            print(colored(f'\n[!] Error: {e}', 'red'))
            break
    print_centered_text('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')


def run():
    global stop_spamming, messages_sent
    messages_sent = 0  # reset the counter
    webhook = stdiomask.getpass(prompt=colored('[?] Webhook url: ', 'white'), mask='*')
    message = input(colored('[?] Message to spam: ', 'white'))
    delay = float(input(colored('[?] Delay in seconds: ', 'white')))

    spam_thread = threading.Thread(target=spam, args=(webhook, message, delay))
    spam_thread.start()

    input()  # just wait for Enter, without printing a message
    stop_spamming = True
    spam_thread.join()

    input(colored("\nPress Enter to return to the main menu.\n", 'white'))