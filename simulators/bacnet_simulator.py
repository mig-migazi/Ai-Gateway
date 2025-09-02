"""
BACnet IP Simulator - Simulates BACnet IP devices for testing
"""

import asyncio
import json
import logging
import socket
import struct
import random
from typing import Dict, Any
from datetime import datetime
import threading

logger = logging.getLogger(__name__)


class BACnetSimulator:
    """Simulates a BACnet IP device"""
    
    def __init__(self, device_id: int = 1234, device_name: str = "Temperature Sensor Simulator"):
        self.device_id = device_id
        self.device_name = device_name
        self.socket = None
        self.running = False
        self.sensor_data = {
            "temperature": 72.5,
            "humidity": 45.2,
            "pressure": 1013.25
        }
    
    async def start(self, port: int = 47808):
        """Start the BACnet simulator"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', port))
            self.socket.settimeout(1.0)
            self.running = True
            
            logger.info(f"BACnet simulator started on port {port}")
            logger.info(f"Device ID: {self.device_id}")
            logger.info(f"Device Name: {self.device_name}")
            
            # Start listening for requests
            await self._listen_for_requests()
        
        except Exception as e:
            logger.error(f"Failed to start BACnet simulator: {e}")
            raise
    
    async def _listen_for_requests(self):
        """Listen for BACnet requests"""
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                logger.info(f"Received request from {addr}")
                
                # Process the request
                response = await self._process_request(data, addr)
                
                if response:
                    self.socket.sendto(response, addr)
                    logger.info(f"Sent response to {addr}")
            
            except socket.timeout:
                continue  # No data received, continue listening
            except Exception as e:
                logger.error(f"Error processing request: {e}")
    
    async def _process_request(self, data: bytes, addr: tuple) -> bytes:
        """Process incoming BACnet request"""
        try:
            # Parse the request
            request_type = self._parse_request_type(data)
            
            if request_type == "who_is":
                return self._create_i_am_response()
            elif request_type == "read_property":
                return self._create_read_property_response(data)
            else:
                logger.warning(f"Unknown request type: {request_type}")
                return None
        
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return None
    
    def _parse_request_type(self, data: bytes) -> str:
        """Parse the type of BACnet request"""
        try:
            # Check for Who-Is request (simplified)
            if len(data) >= 2 and data[-2:] == b'\x10\x08':
                return "who_is"
            
            # Check for ReadProperty request (simplified)
            if len(data) >= 2 and data[-2:] == b'\x00\x0c':
                return "read_property"
            
            return "unknown"
        
        except Exception:
            return "unknown"
    
    def _create_i_am_response(self) -> bytes:
        """Create I-Am response"""
        try:
            # Simulate sensor data variation
            self.sensor_data["temperature"] = 72.0 + random.uniform(-2.0, 2.0)
            self.sensor_data["humidity"] = 45.0 + random.uniform(-5.0, 5.0)
            self.sensor_data["pressure"] = 1013.0 + random.uniform(-10.0, 10.0)
            
            # Create simplified I-Am response
            response = bytearray()
            
            # BACnet/IP header
            response.extend([0x81, 0x0a, 0x00, 0x0c])  # Version, Function, Length
            response.extend([0x00, 0x00, 0x00, 0x00])  # Reserved
            response.extend([0x00, 0x00, 0x00, 0x00])  # Reserved
            
            # BACnet NPDU
            response.extend([0x01, 0x20, 0xff, 0xff])  # Version, Control, Destination, Source
            
            # BACnet APDU - I-Am
            response.extend([0x10, 0x00])  # Unconfirmed-REQ, I-Am
            
            # Device ID and other information would be added here in a real implementation
            
            return bytes(response)
        
        except Exception as e:
            logger.error(f"Error creating I-Am response: {e}")
            return None
    
    def _create_read_property_response(self, request_data: bytes) -> bytes:
        """Create ReadProperty response"""
        try:
            # Create simplified ReadProperty response
            response = bytearray()
            
            # BACnet/IP header
            response.extend([0x81, 0x0a, 0x00, 0x0c])  # Version, Function, Length
            response.extend([0x00, 0x00, 0x00, 0x00])  # Reserved
            response.extend([0x00, 0x00, 0x00, 0x00])  # Reserved
            
            # BACnet NPDU
            response.extend([0x01, 0x20, 0xff, 0xff])  # Version, Control, Destination, Source
            
            # BACnet APDU - ReadProperty ACK
            response.extend([0x30, 0x0c])  # Simple-ACK, ReadProperty
            
            # Property value would be added here in a real implementation
            
            return bytes(response)
        
        except Exception as e:
            logger.error(f"Error creating ReadProperty response: {e}")
            return None
    
    def stop(self):
        """Stop the BACnet simulator"""
        self.running = False
        if self.socket:
            self.socket.close()
        logger.info("BACnet simulator stopped")


async def main():
    """Main entry point for the BACnet simulator"""
    print("Starting BACnet IP Simulator...")
    print("Device ID: 1234")
    print("Device Name: Temperature Sensor Simulator")
    print("Port: 47808")
    print("Press Ctrl+C to stop")
    print()
    
    simulator = BACnetSimulator()
    
    try:
        await simulator.start()
    except KeyboardInterrupt:
        print("\nStopping simulator...")
        simulator.stop()
    except Exception as e:
        print(f"Error: {e}")
        simulator.stop()


if __name__ == "__main__":
    asyncio.run(main())
