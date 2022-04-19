import os
import sqlite3
from pprint import pprint
import re
import yaml
from datetime import timedelta, datetime

regex = r'(?P<mac>\S+) +(?P<ip>\S+) +(\S+) +(\S+) +(?P<vlan>\d+) +(?P<interface>\S+)'


def create_db(name, schema):
    db_exists = os.path.exists(name)
    conn = sqlite3.connect(name)
    if not db_exists:
        print('Создаю базу данных...')
        with open(schema, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
    else:
        print("База данных существует")
    return

def add_data_switches(db_file, filename):
    with open(filename[0]) as f:
        sw_data = yaml.safe_load(f)['switches'].items()
    db_exists = os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_exists:
        for row in sw_data:
            try:
                with conn:
                    query = 'insert into switches (hostname, location) values (?, ?)'
                    conn.execute(query, row)
            except sqlite3.IntegrityError as e:
                print('Error occured: ', e)
    return

def add_data(db_file, filename):
    db_exists = os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_exists:
        for file in filename:
            filename1 = file
            if '/' in file:
                filename1 = file.split('/')[-1]
            sw_name = filename1.split('_')[0]
            with open(file) as f:
                for line in f:
                    match = re.search(regex, line)
                    if match:
                        dict = match.groupdict()
                        try:
                            with conn:
                                query = "INSERT OR REPLACE INTO dhcp (mac, ip, vlan, interface, switch, active, last_active) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))"
                                conn.execute(query, (dict['mac'], dict['ip'], dict['vlan'], dict['interface'], sw_name, 1))
                        except sqlite3.IntegrityError as e:
                            print('Error occured: ', e)
    return

def print_data(data):
    for row in data:
        print(
            '{:20} {:15} {:4} {:20} {:12}'.format(row['mac'], row['ip'], row['vlan'], row['interface'], row['switch']))


def get_data(db_file, key, value):
    db_exists = os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    if db_exists:
        print("\nАктивные записи:")
        query = 'select * from dhcp where {} = ?'.format(key)
        result = conn.execute(query, (value,))
        print_data(result)

        query = 'select count(mac) as count from dhcp where active=0 and {} = ?'.format(key)
        result = conn.execute(query, (value,)).fetchone()
        if result['count'] > 0:
            print("\nНеактивные записи:")
            query = 'select * from dhcp where active=0 and {} = ?'.format(key)
            result = conn.execute(query, (value,))
            print_data(result)



def get_all_data(db_file):
    db_exists = os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    if db_exists:
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


