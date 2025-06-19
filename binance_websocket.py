#!/usr/bin/env python3
import json
import asyncio
import websockets
from kafka import KafkaProducer
import logging
from datetime import datetime
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # Replace with your Kafka server
KAFKA_TOPIC = "binance-crypto-trades"        # Replace with your topic name

# List of symbols you want to subscribe to
SYMBOLS = ["btcusdt", "ethusdt", "bnbusdt", "adausdt", "maticusdt", "solusdt"]  # Add more symbols as needed

# Create a combined stream URL
# Example: wss://fstream.binance.com/stream?streams=btcusdt@trade/ethusdt@trade/bnbusdt@trade
STREAMS = "/".join([f"{symbol}@trade" for symbol in SYMBOLS])
BINANCE_WS_URL = f"wss://fstream.binance.com/stream?streams={STREAMS}"

# Initialize the Kafka producer
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        acks='all',
        retries=3,
        batch_size=16384,
        linger_ms=10
    )
    logger.info(f"Kafka producer initialized for {KAFKA_BOOTSTRAP_SERVERS}")
except Exception as e:
    logger.error(f"Failed to initialize Kafka producer: {e}")
    sys.exit(1)

async def process_websocket_messages():
    while True:
        try:
            async with websockets.connect(BINANCE_WS_URL) as websocket:
                print(f"Connected to Binance WebSocket for symbols: {', '.join(SYMBOLS).upper()}")
                logger.info(f"Publishing to Kafka topic: {KAFKA_TOPIC}")

                while True:
                    message = await websocket.recv()
                    data = json.loads(message)

                    # Each message from combined streams has the following structure:
                    # {
                    #   "stream": "btcusdt@trade",
                    #   "data": { ... trade data ... }
                    # }
                    
                    stream = data.get("stream")
                    trade_data = data.get("data", {})

                    if not stream or not trade_data:
                        print("Invalid message format received.")
                        continue

                    symbol = trade_data.get("s")
                    price = float(trade_data.get("p", 0))
                    quantity = float(trade_data.get("q", 0))
                    timestamp = trade_data.get("T")
                    buyer_maker = trade_data.get("m")
                    trade_id = trade_data.get("t")
                    
                    # Add additional useful fields
                    transformed_data = {
                        "symbol": symbol,
                        "price": price,
                        "quantity": quantity,
                        "timestamp": timestamp,
                        "buyer_maker": buyer_maker,
                        "trade_id": trade_id,
                        "stream": stream,
                        "processing_time": datetime.now().isoformat(),
                        "exchange": "binance",
                        "data_type": "trade"
                    }

                    try:
                        # Publish to Kafka using symbol as key for partitioning
                        future = producer.send(
                            topic=KAFKA_TOPIC,
                            key=symbol,
                            value=transformed_data
                        )
                        
                        # Optional: wait for confirmation (comment out for better performance)
                        # result = future.get(timeout=10)
                        
                        print(f"Published trade for {symbol}: Price={price}, Quantity={quantity}")
                        
                    except Exception as e:
                        logger.error(f"Failed to publish to Kafka: {e}")

        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

def cleanup():
    """Cleanup function to close Kafka producer"""
    try:
        if producer:
            producer.flush()
            producer.close()
            logger.info("Kafka producer closed successfully")
    except Exception as e:
        logger.error(f"Error closing Kafka producer: {e}")

if __name__ == '__main__':
    try:
        print(f"Starting Binance WebSocket stream publisher to Kafka topic: {KAFKA_TOPIC}")
        print(f"Monitoring symbols: {', '.join(SYMBOLS).upper()}")
        print(f"Kafka servers: {KAFKA_BOOTSTRAP_SERVERS}")
        print("Press Ctrl+C to stop...")
        
        asyncio.run(process_websocket_messages())
        
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        cleanup()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        cleanup()
        sys.exit(1)