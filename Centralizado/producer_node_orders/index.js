const amqp = require('amqplib');
const { v4: uuidv4 } = require('uuid');

const RABBIT_HOST = process.env.RABBIT_HOST || 'rabbitmq';
const QUEUE = 'orders_queue';

async function main(){
  const conn = await amqp.connect({ hostname: RABBIT_HOST });
  const ch = await conn.createChannel();
  await ch.assertQueue(QUEUE, { durable: true });

  let i = 0;
  setInterval(async () => {
    const order = {
      id: uuidv4(),
      order_number: `ORD-${Date.now()}`,
      amount: (Math.random() * 100).toFixed(2),
      customer: `customer_${i}`
    };
    ch.sendToQueue(QUEUE, Buffer.from(JSON.stringify(order)), { persistent: true });
    console.log("Sent order:", order);
    i++;
  }, 2500);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
