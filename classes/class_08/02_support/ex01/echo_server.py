#!/usr/bin/env python3
"""Simple TCP/UDP Echo Server using Python's built-in socket module."""

import argparse
import logging
import socket

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BUFFER_SIZE = 1024


def run_tcp_server(host: str, port: int) -> None:
    """Run a blocking TCP echo server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen()
        logger.info("TCP Echo Server listening on %s:%d", host, port)

        while True:
            conn, addr = server_sock.accept()
            with conn:
                logger.info("TCP client connected from %s:%d", addr[0], addr[1])
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        logger.info("TCP client disconnected: %s:%d", addr[0], addr[1])
                        break
                    logger.info("TCP received from %s:%d -> %r", addr[0], addr[1], data.decode(errors="replace"))
                    conn.sendall(data)


def run_udp_server(host: str, port: int) -> None:
    """Run a blocking UDP echo server."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        server_sock.bind((host, port))
        logger.info("UDP Echo Server listening on %s:%d", host, port)

        while True:
            data, addr = server_sock.recvfrom(BUFFER_SIZE)
            logger.info("UDP received from %s:%d -> %r", addr[0], addr[1], data.decode(errors="replace"))
            server_sock.sendto(data, addr)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="TCP/UDP Echo Server")
    parser.add_argument("protocol", choices=["tcp", "udp"], help="Transport protocol to use")
    parser.add_argument("--host", default="127.0.0.1", help="Host address to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9000, help="Port number to listen on (default: 9000)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        if args.protocol == "tcp":
            run_tcp_server(args.host, args.port)
        else:
            run_udp_server(args.host, args.port)
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")


if __name__ == "__main__":
    main()

