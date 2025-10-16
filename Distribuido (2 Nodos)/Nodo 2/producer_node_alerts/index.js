const amqp = require('amqplib');

const RABBIT_HOST = process.env.RABBIT_HOST || 'rabbitmq';
const QUEUE = 'alerts_queue';

async function main(){
  const conn = await amqp.connect({ hostname: RABBIT_HOST });
  const ch = await conn.createChannel();
  await ch.assertQueue(QUEUE, { durable: true });

  let i=0;
  setInterval(() => {
    const alert = {
      id: i,
      severity: i % 2 === 0 ? 'HIGH' : 'LOW',
      message: `Alert number ${i}`
    };
    ch.sendToQueue(QUEUE, Buffer.from(JSON.stringify(alert)), { persistent: true });
    console.log("Sent alert:", alert);
    i++;
  }, 5000);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
