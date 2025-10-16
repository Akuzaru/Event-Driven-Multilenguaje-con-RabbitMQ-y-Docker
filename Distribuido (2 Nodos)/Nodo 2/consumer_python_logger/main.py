import os
import pika
import json

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
EXCHANGE = "logs_exchange"
QUEUE = "logs_queue"

def main():
    params = pika.ConnectionParameters(host=RABBIT_HOST)
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type='fanout', durable=True)
    ch.queue_declare(queue=QUEUE, durable=True)
    ch.queue_bind(queue=QUEUE, exchange=EXCHANGE)

    def callback(ch, method, properties, body):
        msg = json.loads(body)
        print("[LOGGER] Received:", msg)
        # aquí podrías escribir a archivo o DB
        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(queue=QUEUE, on_message_callback=callback)
    print(" [*] Waiting for logs. To exit press CTRL+C")
    try:
        ch.start_consuming()
    except KeyboardInterrupt:
        ch.stop_consuming()
    conn.close()

if __name__ == "__main__":
    main()
