#!/usr/bin/env python3
"""MQTT Telemetry Publisher supporting simulated environmental data and real system metrics."""

import argparse
import json
import logging
import random
import time

import paho.mqtt.client as mqtt
import psutil

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def create_mqtt_client(client_id: str) -> mqtt.Client:
    """Create a Paho MQTT client compatible with both v1.x and v2.x APIs."""
    if hasattr(mqtt, "CallbackAPIVersion"):
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    else:
        client = mqtt.Client(client_id=client_id)

    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            logger.info("Connected to MQTT broker.")
        else:
            logger.error("Failed to connect to MQTT broker (code=%s).", reason_code)

    client.on_connect = on_connect
    return client


class TelemetryGenerator:
    """Generate either simulated environmental readings or real system CPU/RAM telemetry."""

    def __init__(self, mode: str) -> None:
        self.mode = mode
        self.temp = 22.0
        self.humidity = 50.0
        if self.mode == "system":
            # Prime psutil CPU measurement so the first reading is meaningful
            psutil.cpu_percent(interval=None)

    def sample(self) -> tuple[float, float]:
        """Return a tuple (primary_metric, secondary_metric)."""
        if self.mode == "system":
            cpu = round(psutil.cpu_percent(interval=None), 1)
            ram = round(psutil.virtual_memory().percent, 1)
            return cpu, ram

        self.temp = round(min(32.0, max(15.0, self.temp + random.uniform(-0.8, 0.8))), 1)
        self.humidity = round(min(90.0, max(20.0, self.humidity + random.uniform(-2.0, 2.0))), 1)
        return self.temp, self.humidity


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="MQTT Telemetry Publisher")
    parser.add_argument(
        "--mode",
        choices=["env", "system"],
        default="env",
        help="Telemetry source: 'env' (simulated temp/humidity) or 'system' (real CPU/RAM)",
    )
    parser.add_argument("--host", default="localhost", help="MQTT broker host (default: localhost)")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port (default: 1883)")
    parser.add_argument("--topic", default="deti/pico/dht11", help="MQTT topic (default: deti/pico/dht11)")
    parser.add_argument("--interval", type=float, default=2.0, help="Publish interval in seconds (default: 2.0)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client_id = f"iei_publisher_{args.mode}_{random.randint(1000, 9999)}"
    client = create_mqtt_client(client_id)

    logger.info("Connecting to %s:%d (mode=%s, topic=%s)...", args.host, args.port, args.mode, args.topic)
    client.connect(args.host, args.port, keepalive=60)
    client.loop_start()

    generator = TelemetryGenerator(args.mode)

    try:
        while True:
            time.sleep(args.interval)
            primary, secondary = generator.sample()
            payload = {
                "ts": time.time(),
                "t": primary,
                "h": secondary,
                "mode": args.mode,
            }
            client.publish(args.topic, json.dumps(payload), qos=0)
            if args.mode == "system":
                logger.info("Published [system] -> CPU: %.1f%% | RAM: %.1f%%", primary, secondary)
            else:
                logger.info("Published [env] -> Temp: %.1f C | Humidity: %.1f%%", primary, secondary)
    except KeyboardInterrupt:
        logger.info("Publisher stopped by user.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
