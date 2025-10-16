FROM maven:3.8.7-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn -q -DskipTests package

FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/target/producer-java-metrics-1.0.0.jar app.jar
ENV RABBIT_HOST=rabbitmq
CMD ["java", "-jar", "app.jar"]
