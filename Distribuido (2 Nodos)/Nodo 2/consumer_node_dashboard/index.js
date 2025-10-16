const amqp = require('amqplib');

const RABBIT_HOST = process.env.RABBIT_HOST || 'rabbitmq';
const EXCHANGE = 'metrics_exchange';
const EXCHANGE_TYPE = 'topic';
const BINDING_KEY = 'metrics.#';

async function main(){
  const conn = await amqp.connect({ hostname: RABBIT_HOST });
  const ch = await conn.createChannel();
  await ch.assertExchange(EXCHANGE, EXCHANGE_TYPE, { durable: true });
  const q = await ch.assertQueue('', { exclusive: true });
  await ch.bindQueue(q.queue, EXCHANGE, BINDING_KEY);
  console.log("[DASHBOARD] Waiting for metrics...");
  ch.consume(q.queue, msg => {
    if (msg) {
      console.log("[DASHBOARD] Metric:", msg.content.toString());
      ch.ack(msg);
    }
  });
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
