from pprint import pprint
from sys import argv
import sqlite3

db_filename = 'dhcp_snooping.db'

def print_data(data):
    for row in data:
        print(
            '{:20} {:15} {:4} {:20} {:12}'.format(row['mac'], row['ip'], row['vlan'], row['interface'], row['switch']))


if __name__ == "__main__":
    num_args = len(argv) - 1
    conn = sqlite3.connect(db_filename)
    conn.row_factory = sqlite3.Row

    if num_args == 0:
        print('\nВ таблице dhcp такие записи:')
        print("\nАктивные записи:")
        query = 'select * from dhcp where active=1'
        result = conn.execute(query)
        print_data(result)

        query = "select count(mac) as count from dhcp where active=0"
        result = conn.execute(query).fetchone()
        if result['count'] > 0:
            print("\nНеактивные записи:")
            query = 'select * from dhcp where active=0'
            result = conn.execute(query)
            print_data(result)

    elif num_args == 2:
        key, value = argv[1:]
        print('\nИнформация об устройствах с такими параметрами:', key, value)
        query = 'select * from dhcp where {} = ?'.format(key)
        result = conn.execute(query, (value,))
        print_data(result)

        query = 'select count(mac) as count from dhcp where active=0 and {} = ?'.format(key)
        result = conn.execute(query, (value,)).fetchone()
        if result['count'] > 0:
            print("\nНеактивные записи:")
            query = 'select * from dhcp where active=0 and {} = ?'.format(key)
            result = conn.execute(query)
            print_data(result)

    else:
        print("Пожалуйста, введите два или ноль аргументов")
