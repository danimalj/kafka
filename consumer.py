from confluent_kafka import Consumer
import json
import sys

conf = {'bootstrap.servers': 'localhost:9092'
                     , 'group.id': 'mygroup'
                    , 'auto.offset.reset': 'earliest'}

consumer = Consumer(conf)

running = True


def shutdown():
    running = False

def print_msg(msg):
    print('%% %s [%d] at offset %d with key %s:\n' %
          (msg.topic(), msg.partition(), msg.offset(), str(msg.key())))
    print(msg.value())

def KafkaException(error):
    print(f"Kafka Exception: {error}")
    shutdown()

def KafkaError(error):
    print(f"Kafka Error: {error}")
    shutdown()


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=0.1)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                if msg.offset() % 10000 == 0:
                    print_msg(msg)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()



basic_consume_loop(consumer, ['transactions'])