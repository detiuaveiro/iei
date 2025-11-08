#!/usr/bin/env python3

import asyncio
import argparse
import os
import sys
import logging
from tqdm import tqdm

# --- Setup Logger ---
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
# --------------------

CHUNK_SIZE = 1024

class ServerProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()
        self.transfers = {}
        logger.info("Server is ready and waiting for files...")

    def connection_made(self, transport):
        """
        Called when the protocol is initialized. We MUST save the transport.
        """
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            if data.startswith(b'START:'):
                # START:<total_chunks>:<total_size>:<filename>
                parts = data.split(b':', 3)
                total_chunks = int(parts[1])
                total_size = int(parts[2])
                filename = parts[3].decode()
                
                # Initialize state for this new transfer
                self.transfers[addr] = {
                    'filename': filename,
                    'total_chunks': total_chunks,
                    'total_size': total_size,
                    'chunks': {},
                    'received_size': 0
                }
                logger.info(f"Receiving file '{filename}' ({total_size} bytes) from {addr}")

            elif data.startswith(b'DATA:'):
                # DATA:<chunk_num>:<data>
                if addr not in self.transfers:
                    return # Ignore data if no START was received

                parts = data.split(b':', 2)
                chunk_num = int(parts[1])
                chunk_data = parts[2]
                
                # Store chunk if we don't have it already
                if chunk_num not in self.transfers[addr]['chunks']:
                    self.transfers[addr]['chunks'][chunk_num] = chunk_data
                    self.transfers[addr]['received_size'] += len(chunk_data)
                
            elif data == b'END':
                if addr not in self.transfers:
                    return # Ignore
                
                logger.info(f"END signal received from {addr}. Assembling file...")
                self.assemble_file(addr)

        except Exception as e:
            logger.error(f"Error processing packet from {addr}: {e}")

    def assemble_file(self, addr):
        if addr not in self.transfers:
            return

        transfer = self.transfers[addr]
        filename = transfer['filename']
        total_chunks = transfer['total_chunks']
        
        # Check if all chunks are present
        if len(transfer['chunks']) != total_chunks:
            logger.warning(f"File '{filename}' from {addr} is incomplete. "
                           f"Got {len(transfer['chunks'])}/{total_chunks} chunks. Discarding.")
            # We can now safely use self.transport
            self.transport.sendto(b'ACK_FAIL', addr)
        else:
            logger.info(f"Assembling '{filename}' from {addr}...")
            try:
                # Re-assemble in order
                with open(filename, 'wb') as f:
                    for i in range(total_chunks):
                        f.write(transfer['chunks'][i])
                
                logger.info(f"File '{filename}' saved successfully!")
                self.transport.sendto(b'ACK_ALL', addr)
            except IOError as e:
                logger.error(f"Error writing file '{filename}': {e}")
                self.transport.sendto(b'ACK_FAIL', addr)

        # Clean up state for this transfer, ready for the next one
        del self.transfers[addr]

    def connection_lost(self, exc):
        logger.info("Server protocol connection lost (this is unusual but not fatal).")


class ClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, input_file, host, port, finished_event):
        super().__init__()
        self.input_file = input_file
        self.host = host
        self.port = port
        self.finished_event = finished_event # Store the event
        self.chunks = []
        self.filename = os.path.basename(input_file)
        self.total_size = 0
        
    def connection_made(self, transport):
        self.transport = transport
        logger.info(f"Client connected, sending {self.filename} to {self.host}:{self.port}")
        asyncio.create_task(self.send_file())

    async def send_file(self):
        try:
            # First, read the file into chunks
            with open(self.input_file, 'rb') as f:
                while True:
                    data = f.read(CHUNK_SIZE - 50) # Leave room for header
                    if not data:
                        break
                    self.chunks.append(data)
                    self.total_size += len(data)
            
            total_chunks = len(self.chunks)
            logger.info(f"File read. Total chunks: {total_chunks}, Total size: {self.total_size} bytes")

            # 1. Send START packet
            start_message = f"START:{total_chunks}:{self.total_size}:{self.filename}".encode()
            self.transport.sendto(start_message, (self.host, self.port))

            # 2. Send DATA packets with tqdm progress bar
            for i, chunk in enumerate(tqdm(self.chunks, desc=f"Sending {self.filename}")):
                message = b'DATA:%d:' % i + chunk
                self.transport.sendto(message, (self.host, self.port))
                await asyncio.sleep(0.001) # Small delay to avoid buffer overflow

            # 3. Send END packet
            self.transport.sendto(b'END', (self.host, self.port))
            logger.info("File sent. Waiting for server ACK...")

        except FileNotFoundError:
            logger.error(f"Error: File '{self.input_file}' not found.")
            self.transport.close()
        except Exception as e:
            logger.error(f"Error sending file: {e}")
            self.transport.close()

    def datagram_received(self, data, addr):
        if data == b'ACK_ALL':
            logger.info("Server ACK received. Transfer complete.")
        elif data == b'ACK_FAIL':
            logger.error("Server reported transfer failure.")
        else:
            logger.warning(f"Received unknown packet: {data}")
        self.transport.close() # End client session

    def error_received(self, exc):
        logger.error(f"Error received: {exc}")

    def connection_lost(self, exc):
        logger.info("Client connection closed.")
        self.finished_event.set() # Signal main() that we are done

async def main(args):
    loop = asyncio.get_running_loop()

    if args.command == 'receive':
        logger.info(f"Starting persistent UDP server on 0.0.0.0:{args.port}...")
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: ServerProtocol(),
            local_addr=('0.0.0.0', args.port))
        
        # Keep the server running forever
        await asyncio.Event().wait()
        
    elif args.command == 'send':
        logger.info(f"Starting UDP client, sending to {args.host}:{args.port}...")
        finished_event = asyncio.Event()
        
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: ClientProtocol(args.file, args.host, args.port, finished_event),
            remote_addr=(args.host, args.port))
        
        try:
            # Wait for the event, but with a 10-second timeout
            await asyncio.wait_for(finished_event.wait(), timeout=10.0)
        except asyncio.TimeoutError:
            logger.error("Client timed out waiting for server ACK. (Is server running? Is ACK lost?)")
        
    else:
        logger.error("Invalid command.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP File Transfer with asyncio")
    subparsers = parser.add_subparsers(dest="command", required=True)

    recv_parser = subparsers.add_parser('receive', help='Run as persistent server to receive files')
    recv_parser.add_argument('--port', type=int, default=9999, help='Port to listen on')

    send_parser = subparsers.add_parser('send', help='Run as client to send a file')
    send_parser.add_argument('file', type=str, help='File to send')
    send_parser.add_argument('--host', type=str, required=True, help='Server host IP')
    send_parser.add_argument('--port', type=int, default=9999, help='Server port')

    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        logger.info("Shutting down...")