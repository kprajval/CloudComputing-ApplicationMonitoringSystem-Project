from kafka import KafkaConsumer
import json
import psycopg2
import time

# PostgreSQL config
DB_CONFIG = {
    'host': 'postgres',
    'database': 'monitoring',
    'user': 'admin',
    'password': 'admin'
}

# Wait for DB
def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("PostgreSQL is ready.")
            break
        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(2)

# Create logs table if it doesn't exist
def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            topic VARCHAR(50),
            message JSONB,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Start consuming
def consume():
    consumer = KafkaConsumer(
	'api-logs',
    	bootstrap_servers='kafka:9092',
    	group_id='log-consumers',
    	value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    	auto_offset_reset='earliest'
    )

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for msg in consumer:
        cur.execute(
            "INSERT INTO logs (topic, message) VALUES (%s, %s);",
            (msg.topic, json.dumps(msg.value))
        )
        conn.commit()
        print(f"Inserted into DB: {msg.topic} => {msg.value}")

if __name__ == "__main__":
    wait_for_postgres()
    create_table()
    consume()
