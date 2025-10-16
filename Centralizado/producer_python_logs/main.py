import os
import pika
import json
import time
import random

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
EXCHANGE = "logs_exchange"

def connect():
    params = pika.ConnectionParameters(host=RABBIT_HOST)
    return pika.BlockingConnection(params)

def main():
    conn = connect()
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type='fanout', durable=True)
    levels = ["INFO","WARNING","ERROR"]
    i = 0
    try:
        while True:
            msg = {
                "id": i,
                "level": random.choice(levels),
                "message": f"Log message {i}"
            }
            ch.basic_publish(exchange=EXCHANGE, routing_key='', body=json.dumps(msg))
            print("Sent:", msg)
            i += 1
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    main()
