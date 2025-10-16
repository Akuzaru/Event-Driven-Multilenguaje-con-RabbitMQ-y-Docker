package edu.example;

import com.rabbitmq.client.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;

public class App {
    private static final String QUEUE = "orders_queue";
    public static void main(String[] args) throws Exception {
        String host = System.getenv().getOrDefault("RABBIT_HOST", "rabbitmq");
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(host);
        try (Connection conn = factory.newConnection();
             Channel ch = conn.createChannel()) {
            ch.queueDeclare(QUEUE, true, false, false, null);
            System.out.println("[BILLING] Waiting for orders...");
            DeliverCallback deliverCallback = (consumerTag, delivery) -> {
                String body = new String(delivery.getBody(), StandardCharsets.UTF_8);
                System.out.println("[BILLING] Received order: " + body);
                // Simulate billing processing
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) { }
                ch.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
                System.out.println("[BILLING] Processed order");
            };
            ch.basicConsume(QUEUE, false, deliverCallback, consumerTag -> {});
            // keep main thread alive
            while (true) {
                Thread.sleep(1000);
            }
        }
    }
}
