import argparse
import signal
import logging
from confluent_kafka import Consumer

def shutdown(signum, frame):
    global running
    print("Shutting down Kafka consumer gracefully...")
    running = False

import argparse
import logging
import signal

def main():
    """
    Kafka Consumer main function.

    Args:
        --topic (str): Kafka topic to consume messages from.
        --broker (str): Kafka broker to connect to.
        --group (str): Consumer group to join.
        --offset (str, optional): Offset to start consuming from. Defaults to "earliest".
        --commit-count (int, optional): Number of messages to consume before committing. Defaults to 100.
    """
    parser = argparse.ArgumentParser(description="Kafka Consumer")
    parser.add_argument("--topic", required=True, help="Kafka topic")
    parser.add_argument("--broker", required=True, help="Kafka broker to connect to")
    parser.add_argument("--group", required=True, help="Consumer group")
    parser.add_argument("--offset", default="earliest", help="Offset to start consuming from")
    parser.add_argument("--commit-count", type=int, default=100, help="Number of messages to consume before committing")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    conf = {'bootstrap.servers': args.broker, 'group.id': args.group, 'auto.offset.reset': args.offset}
    consumer = Consumer(conf)

    try:
        consumer.subscribe([args.topic])
        counter = 0
        while running:
            msg = consumer.poll(timeout=0.1)
            if msg is None:
                continue
            counter += 1

            if counter == args.commit_count:
                logger.info(f"Committing offset at {msg.offset()} as a safety measure.")
                consumer.commit()
                counter = 0

            if msg.error():
                logger.error(f"Kafka Error: {msg.error()}")
                # Handle other exceptions as needed

    finally:
        consumer.close()

if __name__ == "__main__":
    running = True
    main()
