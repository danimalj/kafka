import argparse
import signal
import sys
import logging
from confluent_kafka import Producer
from faker import Faker
import json

def shutdown(signum, frame):
    global running
    print("Shutting down Kafka producer gracefully...")
    running = False

def fake_account():
    fake = Faker()
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

import argparse
import sys
import signal
import logging
from confluent_kafka import Producer

def main():
    """
    Kafka Producer

    This script produces messages to a Kafka topic using a Kafka broker.
    It takes command line arguments for the topic, broker, commit count, and test messages.

    Args:
        --topic (str): Kafka topic to produce messages to (required)
        --broker (str): Kafka broker to connect to (required)
        -c, --commit-count (int): Number of messages to produce before committing (default: 100000)
        -m, --test-messages (int): Number of messages to produce (default: 100000)

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument("--topic", required=True, help="Kafka topic")
    parser.add_argument("--broker", required=True, help="Kafka broker to connect to")
    parser.add_argument("-c", "--commit-count", type=int, default=100000, help="Number of messages to produce before committing")
    parser.add_argument("-m", "--test-messages", type=int, default=100000, help="Number of messages to produce")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    try:
        topic = args.topic
        broker = args.broker
        commit_count = args.commit_count
        test_messages = args.test_messages

        producer = Producer({'bootstrap.servers': broker})
        logger.info(f"Producing messages to topic: {topic}")
        logger.info(f"Connecting to Kafka broker: {broker}")

        for i in range(test_messages):
            transaction = dict_to_bytestring(fake_account())
            producer.produce(topic, transaction)
            if i % commit_count == 0:
                logger.info(f"Produced message number: {i}")
                producer.flush()

        producer.flush()
        ret_code = 0

    except Exception as e:
        logger.error(f"Exception: {e}")
        logger.error(f"Could not connect to Kafka broker {broker}")
        ret_code = 1

    finally:
        exit(ret_code)

if __name__ == "__main__":
    running = True
    main()