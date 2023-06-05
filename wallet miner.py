import json
import random
import string
import time
import threading
import requests
from termcolor import colored
from urllib.parse import urlparse
import datetime
import os
import secrets
import bitcoin
def generate_private_key():
    """Generate a random 32-byte hex Bitcoin private key"""
    private_key = secrets.token_bytes(32)
    return bitcoin.encode_privkey(private_key, 'wif')
def private_to_public(private_key):
    """Convert private key to public key"""
    return bitcoin.privkey_to_pubkey(private_key)

def public_to_address(public_key):
    """Convert public key to Bitcoin address"""
    return bitcoin.pubkey_to_address(public_key)

def random_wallet_software():
    wallet_softwares = {
        'Bitcoin Core': 'https://bitcoincore.org/',
        'Electrum': 'https://electrum.org/',
        'BitPay': 'https://bitpay.com/',
        'Breadwallet': 'https://brd.com/',
        'Mycelium': 'https://wallet.mycelium.com/',
        'Jaxx': 'https://jaxx.io/',
        'Armory': 'https://www.bitcoinarmory.com/',
        'GreenAddress': 'https://greenaddress.it/en/',
        'Coinomi': 'https://www.coinomi.com/',
        'Exodus': 'https://www.exodus.com/'
    }
    wallet, link = random.choice(list(wallet_softwares.items()))
    return wallet, link




WORDS_FILE_PATH = "words.txt"  # This path might vary based on your OS
SETTINGS_FILE_PATH = "settings.json"
def get_btc_usd():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
    price_usd = response.json()['bpi']['USD']['rate_float']
    return price_usd
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def run():
    
    # Load settings
    with open(SETTINGS_FILE_PATH, 'r') as file:
        settings = json.load(file)

    # Check if webhook is set
    if 'discord_webhook' not in settings or not is_valid_url(settings['discord_webhook']):
        while True:
            webhook = input(colored('[?] Webhook url: ', 'white'))
            if is_valid_url(webhook):
                settings['discord_webhook'] = webhook
                break
            else:
                print(colored("Invalid URL. Please enter a valid URL.", 'red'))


    # Ask user for number of threads
    num_threads = int(input(colored('[?] Number of threads: ', 'white')))

    # Load words
    with open(WORDS_FILE_PATH, 'r') as file:
        words = file.read().splitlines()

    # Start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=generate_addresses, args=(words, settings['discord_webhook']))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    input(colored("\nPress Enter to return to the main menu.\n", 'white'))
def send_initial_message(webhook, data):
    response = requests.post(webhook, json=data)
    return response.json()  # Return the response to get the message ID
def edit_message(webhook, message_id, new_data):
    requests.patch(f'{webhook}/messages/{message_id}', json=new_data)

def generate_addresses(words, webhook):
    # Generate 5 addresses
    tries = 0
    hits = 0
    hit_times = []

    start_time = time.time()
    for i in range(10):
        # Generate random address
        address = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(24, 32)))

        # Generate 20 random words
        random_words = ' '.join(f'{i+1}. {word}' for i, word in enumerate(random.choices(words, k=20)))

        # Print address and words
        print(colored(f'[INVALID] {address} {random_words}', 'red'))

        # Sleep for a bit to simulate spamming
        time.sleep(0.1)

        # Print line breaks
        print('\n' * 1)

        tries += 1


    # Generate a valid address and words
    valid_address = generate_private_key()
    valid_words = ' '.join(random.choices(words, k=20))

    # Print valid address and words with a [VALID] label
    print(colored(f'[VALID] {valid_address} {valid_words}', 'green'))
    # Increase the number of hits and record the time
    hits += 1
    hit_time = time.time() - start_time
    hit_times.append(hit_time)
    # Send webhook message
        # Update console title with new statistics
    avg_hit_time = sum(hit_times) / len(hit_times)
    time_taken = time.time() - start_time
    btc = random.uniform(0.001, 0.01)
    btc_usd = btc * get_btc_usd()
    timestamp = int(datetime.datetime.now().timestamp())
    date = f'<t:{timestamp}:f>'
    os.system(f'title Mined: {btc:.3f} BTC ~ {btc_usd:.2f} USD  Miss: {tries - hits} / Hit: {hits} / Miss/Hit: {((tries - hits) / hits) if hits else 0:.2f}  Avg Hit: {avg_hit_time:.2f} seconds')
    public_key = private_to_public(valid_address)
    btc_adress = public_to_address(public_key)

    all_values = f"\n**` 🔒 Private `**\n {valid_address}\n\n` 🔓 Public ` {public_key}\n\n` 📧 Address `\n {btc_adress}"
    with open(SETTINGS_FILE_PATH, 'r') as file:
        settings = json.load(file)
    user_id = settings.get('user_id', 'User ID not set')

    data = {
        "embeds": [{
            "color": 0x2c3134,
            "title": "",
            "description": f"` ➤ `   {user_id}\n` ➤ `   took {time_taken:.2f}s",
            "fields": [
                {
                    "name": "` ! ` Keys ",
                    "value": all_values,
                    "inline": False
                },
                {
                    "name": "` ? ` Transfered to",
                    "value": settings['bitcoin_address'],
                    "inline": True
                },
                {
                    "name": "` ? ` Wallet Software",
                    "value": f"[{random_wallet_software()[0]}]({random_wallet_software()[1]})",
                    "inline": True
                },

                

                {
                    "name": "` ? ` Current BTC",
                    "value": f"{btc:.3f} BTC ~ {btc_usd:.2f} USD",
                    "inline": True
                },
                {
                    "name": "` ? ` Generated at",
                    "value": date,
                    "inline": True
                },
                {
                    "name": "` ? ` 2FA",
                    "value": "Yes",
                    "inline": True
                },
                {
                    "name": "` ? ` Network Fees",
                    "value": f"{random.uniform(0.0001, 0.001):.4f} BTC",
                    "inline": True
                },
                {
                    "name": "` * ` Word list (20/20)",
                    "value": f"```\n{random_words}\n```",
                    "inline": False
                }
            ],
            "footer": {
            "text": f"Hit achieved in {time_taken:.2f} Hours | made by reverse®"
        },
       
        # "image": {
        #     "url": "https://cdn.discordapp.com/attachments/1090633507933536398/1112363858091323413/Nowy_projekt.png"
        # }
        }]
    }

    requests.post(webhook, json=data)
    time.sleep(1)
    # Generate initial embed
    initial_embed = {
        "embeds": [{
            "title": "Transfering by vps SSH ~",
            "description": f"```bf\n[POST]: Sending Request\n[POST]: Sucessfully Sent\n[SENT]: {btc_usd:.2f}$\n[!INFORMATIONS]:\n -\n```",
            "color": 0x2c3134,
            "image": {
                "url": "https://cdn.discordapp.com/attachments/1090633507933536398/1112370861563977728/Nowy_projekt_1.png"
            },
            "footer": {
            "text": f"Output: {btc:.3f} BTC ~ {btc_usd:.2f} USD | made by reverse ® | "
        },
        }]
    }

    # Send the initial message
    requests.post(webhook, json=initial_embed)
