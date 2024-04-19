from confluent_kafka import Producer
from faker import Faker
import json


fake = Faker()


def fake_account():
    return {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'account': fake.iban(),
        'amount': fake.random_int(min=1000, max=10000)
    }


def dict_to_bytestring(json_dict):
    str_dict = json.dumps(json_dict)
    bytestring = bytes(str_dict, 'utf-8')
    return bytestring

try:
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    print("Connection to Kafka broker successful")

    for i in range(100000):
        transaction = dict_to_bytestring(fake_account())
        producer.produce('transactions', transaction)
        if i % 10000 == 0:
            print(f"Produced message number: {i}")
            producer.flush()
    producer.flush()
    ret_code = 0
except Exception as e:
    print(f"Exception: {e}")
    print("Could not connect to Kafka broker")
    ret_code = 1

finally:
    exit(ret_code)
