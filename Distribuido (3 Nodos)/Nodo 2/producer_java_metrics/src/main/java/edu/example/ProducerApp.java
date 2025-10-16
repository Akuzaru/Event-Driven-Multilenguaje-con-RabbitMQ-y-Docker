package edu.example;

import com.rabbitmq.client.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

public class ProducerApp {
    private static final String EXCHANGE = "metrics_exchange";
    public static void main(String[] args) throws Exception {
        String host = System.getenv().getOrDefault("RABBIT_HOST", "rabbitmq");
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(host);
        try (Connection conn = factory.newConnection();
             Channel ch = conn.createChannel()) {
            ch.exchangeDeclare(EXCHANGE, BuiltinExchangeType.TOPIC, true);
            ObjectMapper om = new ObjectMapper();
            int i = 0;
            while (true) {
                Map<String,Object> m = new HashMap<>();
                m.put("id", i);
                m.put("cpu", Math.random()*100);
                m.put("mem", Math.random()*100);
                String body = om.writeValueAsString(m);
                String routing = "metrics.system";
                ch.basicPublish(EXCHANGE, routing, null, body.getBytes(StandardCharsets.UTF_8));
                System.out.println("[METRICS] Sent: " + body);
                Thread.sleep(3000);
                i++;
            }
        }
    }
}
