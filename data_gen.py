import requests
import json
import signal
import sys
import psycopg2
import random
import faker_commerce
from psycopg2 import Error
from time import sleep
from faker import Faker


def signal_handler(signal, frame):
    index = read_index()
    write_index(index + 2)
    sys.exit(0)


def write_index(index):
    with open('counter', 'w+') as val:
        val.write(str(index))
    return


def read_index(): 
    try:
        with open('counter', 'r+') as val:
            index = int(val.readline())
    except FileNotFoundError as e:
            index = 1
    return index


def connect_to_table(config_json):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=config_json['user'],
                                      password=config_json['password'],
                                      host=config_json['host'],
                                      port=config_json['port'],
                                      database=config_json['database'])

        # Create a cursor to perform database operations
        # cursor = connection.cursor()
        return connection

    except (Exception, Error) as error:
        return None

def write_to_table(data, connection, config_json):
    insert_query = f"INSERT INTO {config_json['schema']}.{config_json['table']} (id, product_name, rating," \
                   f"review_count, image_url, date_uploaded, seller_name, delivery_estimate_days, product_desc) VALUES ({data['index']}, " \
                   f"'{data['product_name']}', {data['rating']}, {data['review_count']}, " \
                   f"'{data['image_url']}', '{data['date_uploaded']}', '{data['seller_name']}', {data['delivery_estimate_days']}, '{data['product_desc']}'" \
                   f")"
    cursor = connection.cursor()
    cursor.execute(insert_query)
    connection.commit()
    return


def main():
    with open('data_gen_config.json', 'r') as config_file:
        config_json = json.load(config_file)

    db_connection = connect_to_table(config_json)
    if db_connection == None:
        print(f"Failed to connect to the database {config_json['database']}")
        return

    g_index = read_index()
    signal.signal(signal.SIGINT, signal_handler)
    fake = Faker()
    fake.add_provider(faker_commerce.Provider)
    while True:
        data = {}

        data['index'] = g_index
        data['product_name'] = fake.ecommerce_name()
        data['product_desc'] = fake.text()
        data['rating'] = fake.pyfloat(left_digits=1, right_digits=2, min_value=0.5, max_value=4.99)
        data['review_count'] = fake.pyint(min_value=1, max_value=4000)
        data['delivery_estimate_days'] = fake.pyint(min_value=1, max_value=9)
        data['image_url'] = fake.image_url()
        data['seller_email'] = fake.email()
        data['seller_name'] = fake.company()
        data['date_uploaded'] = str(fake.date_this_year(True, True))
 
        data_json = json.dumps(data)
        data_json = bytes(str(data_json), 'utf-8')
        write_to_table(data, db_connection, config_json)
        print(f"Inserted entry {g_index} to table {config_json['table']}")
        g_index += 1
        write_index(g_index)
        sleep(5)


main()
