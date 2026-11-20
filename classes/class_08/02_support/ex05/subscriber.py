#!/usr/bin/env python3
"""MQTT Telemetry Subscriber that logs incoming readings and triggers threshold alerts."""

import argparse
import json
import logging
import random

import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="MQTT Telemetry Alert Subscriber")
    parser.add_argument("--host", default="localhost", help="MQTT broker host (default: localhost)")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port (default: 1883)")
    parser.add_argument("--topic", default="deti/pico/dht11", help="MQTT topic or wildcard (default: deti/pico/dht11)")
    parser.add_argument(
        "--threshold",
        type=float,
        default=28.0,
        help="Alert threshold for primary metric (Temp C or CPU %%) (default: 28.0)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client_id = f"iei_subscriber_{random.randint(1000, 9999)}"

    if hasattr(mqtt, "CallbackAPIVersion"):
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    else:
        client = mqtt.Client(client_id=client_id)

    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            logger.info("Connected to %s:%d. Subscribing to '%s'...", args.host, args.port, args.topic)
            client.subscribe(args.topic)
        else:
            logger.error("Connection failed (code=%s).", reason_code)

    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
        except json.JSONDecodeError:
            logger.warning("Invalid JSON on %s: %r", msg.topic, msg.payload)
            return

        mode = data.get("mode", "env")
        primary = data.get("t")
        secondary = data.get("h")

        if mode == "system":
            logger.info("[%s] CPU: %s%% | RAM: %s%%", msg.topic, primary, secondary)
        else:
            logger.info("[%s] Temp: %s C | Humidity: %s%%", msg.topic, primary, secondary)

        if isinstance(primary, (int, float)) and primary >= args.threshold:
            logger.warning("ALERT on %s: value %.1f exceeded threshold %.1f!", msg.topic, primary, args.threshold)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(args.host, args.port, keepalive=60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Subscriber stopped by user.")
        client.disconnect()


if __name__ == "__main__":
    main()

