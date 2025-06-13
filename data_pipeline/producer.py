import time
import csv
import json
from kafka import KafkaProducer
import os

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = 'insurance_data_stream'
CSV_FILE_PATH = 'data_source/insurance.csv'
SIMULATION_DELAY_SECONDS = 0.01 # Jeda waktu antar pengiriman pesan

def create_producer():
    """Membuat dan mengembalikan instance KafkaProducer."""
    print(f"Connecting to Kafka Broker at {KAFKA_BROKER}...")
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(0, 10, 2) # Sesuaikan jika versi Kafka berbeda
        )
        print("Successfully connected to Kafka Broker.")
        return producer
    except Exception as e:
        print(f"Failed to connect to Kafka Broker: {e}")
        time.sleep(5)
        return create_producer()

def publish_data(producer, topic):
    """Membaca data dari CSV dan mengirimkannya ke Kafka."""
    print(f"Reading data from {CSV_FILE_PATH} and publishing to topic '{topic}'...")
    
    with open(CSV_FILE_PATH, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            try:
                message = {
                    "age": int(row["age"]),
                    "sex": row["sex"],
                    "bmi": float(row["bmi"]),
                    "children": int(row["children"]),
                    "smoker": row["smoker"],
                    "region": row["region"],
                    "charges": float(row["charges"])
                }
                
                producer.send(topic, value=message)
                print(f"Sent: {message}")
                
                time.sleep(SIMULATION_DELAY_SECONDS)
                
            except (ValueError, KeyError) as e:
                print(f"Skipping row due to data error: {row}. Error: {e}")
                continue
    
    producer.flush()
    print("All data has been sent.")

if __name__ == "__main__":
    kafka_producer = create_producer()
    if kafka_producer:
        publish_data(kafka_producer, KAFKA_TOPIC)
        kafka_producer.close()
        print("Producer has been closed.")
