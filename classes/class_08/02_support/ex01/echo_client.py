#!/usr/bin/env python3
"""Simple TCP/UDP Echo Client using Python's built-in socket module."""

import argparse
import logging
import socket

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BUFFER_SIZE = 1024


def run_tcp_client(host: str, port: int, message: str) -> None:
    """Connect to a TCP echo server, send a message, and log the reply."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((host, port))
        client_sock.sendall(message.encode())
        data = client_sock.recv(BUFFER_SIZE)
        logger.info("TCP echo received: %r", data.decode(errors="replace"))


def run_udp_client(host: str, port: int, message: str) -> None:
    """Send a UDP datagram to an echo server and log the reply."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_sock:
        client_sock.settimeout(5.0)
        client_sock.sendto(message.encode(), (host, port))
        data, addr = client_sock.recvfrom(BUFFER_SIZE)
        logger.info("UDP echo received from %s:%d -> %r", addr[0], addr[1], data.decode(errors="replace"))


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="TCP/UDP Echo Client")
    parser.add_argument("protocol", choices=["tcp", "udp"], help="Transport protocol to use")
    parser.add_argument("--host", default="127.0.0.1", help="Server host address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9000, help="Server port number (default: 9000)")
    parser.add_argument("--message", default="Ola, IEI!", help="Message to send (default: 'Ola, IEI!')")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.protocol == "tcp":
        run_tcp_client(args.host, args.port, args.message)
    else:
        run_udp_client(args.host, args.port, args.message)


if __name__ == "__main__":
    main()

