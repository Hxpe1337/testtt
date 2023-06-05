import requests
import prettytable
import stdiomask
from termcolor import colored
from shutil import get_terminal_size

def print_centered_text(text):
    terminal_width = get_terminal_size().columns
    colors = ['red', 'light_red']  # Different shades of purple
    for i, line in enumerate(text.splitlines()):
        print(colored(line.center(terminal_width), colors[i%len(colors)]))

def run():
    address = stdiomask.getpass(prompt=colored('[?] Bitcoin address: ', 'white'), mask='*')
    response = requests.get(f'https://api.blockcypher.com/v1/btc/main/addrs/{address}/full')
    if response.status_code == 200:
        address_info = response.json()
        display_address_info(address_info)
    else:
        print(colored(f"[!] Error: {response.json()['error']}", 'red'))

def display_address_info(address_info):
    table = prettytable.PrettyTable()
    table.field_names = ['Field', 'Value']
    table.align = 'l'

    balance_in_btc = address_info['balance'] / 100000000
    final_balance_in_btc = address_info['final_balance'] / 100000000
    total_received_in_btc = address_info['total_received'] / 100000000
    total_sent_in_btc = address_info['total_sent'] / 100000000
    unconfirmed_balance_in_btc = address_info['unconfirmed_balance'] / 100000000

    table.add_row(['Address', address_info['address']])
    table.add_row(['Balance (BTC)', balance_in_btc])
    table.add_row(['Final Balance (BTC)', final_balance_in_btc])
    table.add_row(['Total Received (BTC)', total_received_in_btc])
    table.add_row(['Total Sent (BTC)', total_sent_in_btc])
    table.add_row(['Unconfirmed Balance (BTC)', unconfirmed_balance_in_btc])
    table.add_row(['Number of Transactions', address_info['n_tx']])

    print_centered_text('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print_centered_text("\nBitcoin Address Information:\n")
    print_centered_text(str(table))

    # Transaction history
    if 'txrefs' in address_info:
        transaction_table = prettytable.PrettyTable()
        transaction_table.field_names = ['Transaction Hash', 'Block Height', 'Date', 'Value (BTC)']
        transaction_table.align = 'l'

        for tx in address_info['txrefs']:
            if 'confirmations' in tx:
                value_in_btc = tx['value'] / 100000000
                transaction_table.add_row([tx['tx_hash'], tx['block_height'], tx['confirmed'], value_in_btc])

        print_centered_text("\nTransaction History:\n")
        print_centered_text(str(transaction_table))
    else:
        print_centered_text("\nNo transactions associated with this address.\n")

    print_centered_text('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

    input(colored("\nPress Enter to return to the main menu.\n", 'white'))


if __name__ == '__main__':
    run()
