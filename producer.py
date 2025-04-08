# producer.py

from kafka import KafkaProducer
import json
import time
import socket

# Wait for Kafka broker to be ready
def wait_for_kafka(host='kafka', port=9092, timeout=60):
    print("Waiting for Kafka to be ready...")
    for _ in range(timeout):
        try:
            with socket.create_connection((host, port), timeout=2):
                print("Kafka is ready!")
                return
        except OSError:
            time.sleep(1)
    raise Exception("Kafka broker not available after waiting.")

# Call wait before producer init
wait_for_kafka()

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retries=5
)

# Send logs
def send_logs():
    for i in range(10):
        log = {
            "message": f"Log message {i}",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        producer.send("api-logs", value=log)
        print("Sent:", log)
        time.sleep(2)

if __name__ == "__main__":
    send_logs()
    producer.flush()
    producer.close()
