import os
import pika
import json

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
QUEUE = "alerts_queue"

def main():
    params = pika.ConnectionParameters(host=RABBIT_HOST)
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.queue_declare(queue=QUEUE, durable=True)

    def cb(ch, method, properties, body):
        alert = json.loads(body)
        print("[ALERTS] Received:", alert)
        # Simulate sending a notification (email, webhook...)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(queue=QUEUE, on_message_callback=cb)
    print(" [*] Waiting for alerts. To exit press CTRL+C")
    try:
        ch.start_consuming()
    except KeyboardInterrupt:
        ch.stop_consuming()
    conn.close()

if __name__ == "__main__":
    main()
