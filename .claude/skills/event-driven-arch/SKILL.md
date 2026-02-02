---
name: event-driven-arch
description: Design and implement scalable event-driven architectures using Kafka, Dapr, and pub/sub patterns for microservices.
---

# Event-Driven Architecture

## Instructions

1. **System design**
   - Identify event producers, consumers, and brokers
   - Define asynchronous communication boundaries
   - Ensure loose coupling between microservices

2. **Kafka fundamentals**
   - Create and manage Kafka topics
   - Configure partitions and replication factors
   - Implement producers and consumers
   - Handle offsets, retries, and error scenarios

3. **Pub/Sub patterns**
   - Apply publish/subscribe for inter-service communication
   - Design fan-out and event streaming use cases
   - Ensure idempotent event handling

4. **Platform setup**
   - Work with Redpanda Cloud or self-hosted Kafka clusters
   - Configure local and cloud-based environments
   - Secure Kafka with authentication and authorization

5. **Dapr integration**
   - Use Dapr Pub/Sub with Kafka or Redpanda
   - Implement State Management for event-driven workflows
   - Use Bindings for external systems
   - Manage Secrets securely
   - Enable Service Invocation for sync calls when required

6. **Event contracts**
   - Design clear event schemas (JSON, Avro, or Protobuf)
   - Version events safely without breaking consumers
   - Validate and document message contracts

## Best Practices

- Prefer events over direct service calls
- Keep events immutable and self-describing
- Design for at-least-once delivery
- Handle duplicate events gracefully
- Version schemas explicitly
- Monitor lag, throughput, and failures
- Separate command and event topics

## Example Structure

```yaml
# Kafka Topic
name: order.created
partitions: 6
replicationFactor: 3
