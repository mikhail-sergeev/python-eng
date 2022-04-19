import os
import sqlite3
from pprint import pprint
import re
import yaml
from datetime import timedelta, datetime


db_filename = 'dhcp_snooping.db'
switches_file = "switches.yml"
switches_list = ['new_data/sw1_dhcp_snooping.txt', 'new_data/sw2_dhcp_snooping.txt', 'new_data/sw3_dhcp_snooping.txt']

regex = r'(?P<mac>\S+) +(?P<ip>\S+) +(\S+) +(\S+) +(?P<vlan>\d+) +(?P<interface>\S+)'

def fill_switches(conn):
    with open(switches_file) as f:
        sw_data = yaml.safe_load(f)['switches'].items()
    for row in sw_data:
        try:
            with conn:
                query = 'insert into switches (hostname, location) values (?, ?)'
                conn.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)
    return

def cleanup_dhcp(conn):
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    try:
        with conn:
            query = "DELETE  FROM dhcp WHERE last_active < '{}'".format(week_ago)
            conn.execute(query)
    except sqlite3.IntegrityError as e:
        print('Error occured: ', e)

    return

def fill_dhcp(filename, conn):
    filename1 = filename
    if '/' in filename:
        filename1 = filename.split('/')[-1]
    sw_name = filename1.split('_')[0]

    with open(filename) as f:
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

if __name__ == "__main__":
    db_exists = os.path.exists(db_filename)
    connection = sqlite3.connect(db_filename)

    if not db_exists:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
    else:
        print("Добавляю данные в таблицу switches...")
        fill_switches(connection)

        try:
            with connection:
                query = 'UPDATE dhcp SET active = 0'
                connection.execute(query)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)

        print("Добавляю данные в таблицу dhcp...")
        for sw in switches_list:
            fill_dhcp(sw, connection)

        cleanup_dhcp(connection)
        connection.close()







