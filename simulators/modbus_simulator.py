#!/usr/bin/env python3
"""
Modbus TCP Simulator
Simulates a Modbus TCP device for industrial automation
"""

import asyncio
import json
import logging
import random
import socket
import struct
import time
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModbusTCPSimulator:
    """Simulates a Modbus TCP device"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 502):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
        # Device information (this would come from PDF documentation)
        self.device_info = {
            "device_type": "modbus_tcp_device",
            "manufacturer": "Schneider Electric",
            "model": "Modicon M580 PLC",
            "firmware_version": "2.80",
            "device_id": 1,
            "unit_id": 1,
            "description": "Programmable Logic Controller for industrial automation"
        }
        
        # Modbus register map (from device documentation)
        self.register_map = {
            # Input Registers (3x) - Read-only
            30001: {"name": "Temperature_Sensor_1", "type": "float", "unit": "°C", "value": 22.5, "range": (0, 100)},
            30002: {"name": "Temperature_Sensor_2", "type": "float", "unit": "°C", "value": 23.1, "range": (0, 100)},
            30003: {"name": "Pressure_Sensor", "type": "float", "unit": "bar", "value": 2.5, "range": (0, 10)},
            30004: {"name": "Flow_Rate", "type": "float", "unit": "L/min", "value": 45.2, "range": (0, 100)},
            30005: {"name": "Vibration_Level", "type": "float", "unit": "mm/s", "value": 0.8, "range": (0, 20)},
            30006: {"name": "Motor_Speed", "type": "int", "unit": "RPM", "value": 1450, "range": (0, 3000)},
            30007: {"name": "Power_Consumption", "type": "float", "unit": "kW", "value": 15.3, "range": (0, 50)},
            30008: {"name": "System_Status", "type": "int", "unit": "", "value": 1, "range": (0, 3)},  # 0=Stop, 1=Run, 2=Error, 3=Maintenance
            
            # Holding Registers (4x) - Read/Write
            40001: {"name": "Setpoint_Temperature", "type": "float", "unit": "°C", "value": 25.0, "range": (15, 35)},
            40002: {"name": "Setpoint_Pressure", "type": "float", "unit": "bar", "value": 2.0, "range": (1, 5)},
            40003: {"name": "Control_Mode", "type": "int", "unit": "", "value": 1, "range": (0, 2)},  # 0=Manual, 1=Auto, 2=Remote
            40004: {"name": "Alarm_Threshold", "type": "float", "unit": "°C", "value": 30.0, "range": (20, 40)},
            40005: {"name": "Maintenance_Interval", "type": "int", "unit": "days", "value": 30, "range": (1, 365)},
            40006: {"name": "Calibration_Date", "type": "int", "unit": "days_since_epoch", "value": 19423, "range": (0, 99999)},
        }
        
        # Coils (0x) - Read/Write
        self.coil_map = {
            1: {"name": "Motor_Start", "value": True, "description": "Motor start/stop control"},
            2: {"name": "Pump_Enable", "value": False, "description": "Pump enable/disable"},
            3: {"name": "Alarm_Reset", "value": False, "description": "Alarm reset button"},
            4: {"name": "Maintenance_Mode", "value": False, "description": "Maintenance mode enable"},
            5: {"name": "Remote_Control", "value": True, "description": "Remote control enable"},
        }
        
        # Discrete Inputs (1x) - Read-only
        self.discrete_input_map = {
            10001: {"name": "Emergency_Stop", "value": False, "description": "Emergency stop button status"},
            10002: {"name": "Door_Open", "value": False, "description": "Control panel door status"},
            10003: {"name": "Power_Supply_OK", "value": True, "description": "Power supply status"},
            10004: {"name": "Communication_OK", "value": True, "description": "Communication status"},
            10005: {"name": "Sensor_Fault", "value": False, "description": "Sensor fault indicator"},
        }
        
        # Error codes and troubleshooting (from documentation)
        self.error_codes = {
            0x01: "Illegal Function - Function code not supported",
            0x02: "Illegal Data Address - Register address not supported",
            0x03: "Illegal Data Value - Data value not in valid range",
            0x04: "Slave Device Failure - Device internal error",
            0x05: "Acknowledge - Request accepted but processing delayed",
            0x06: "Slave Device Busy - Device is processing another request",
            0x08: "Memory Parity Error - Memory parity error detected",
            0x0A: "Gateway Path Unavailable - Gateway cannot process request",
            0x0B: "Gateway Target Device Failed - Target device failed to respond"
        }
        
        # Troubleshooting steps (from documentation)
        self.troubleshooting = {
            "communication_error": [
                "Check network cable connection",
                "Verify IP address and port configuration",
                "Check device power supply",
                "Verify Modbus TCP settings",
                "Test with Modbus client software"
            ],
            "sensor_fault": [
                "Check sensor wiring connections",
                "Verify sensor power supply",
                "Check sensor calibration",
                "Replace faulty sensor if necessary",
                "Update sensor configuration"
            ],
            "motor_fault": [
                "Check motor power supply",
                "Verify motor control wiring",
                "Check motor overload protection",
                "Inspect motor for mechanical issues",
                "Reset motor protection devices"
            ],
            "pressure_anomaly": [
                "Check pressure sensor calibration",
                "Verify pressure line connections",
                "Check for leaks in pressure system",
                "Verify pressure setpoint configuration",
                "Inspect pressure relief valves"
            ]
        }
    
    async def start(self):
        """Start the Modbus TCP simulator"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            logger.info(f"🔧 Modbus TCP Simulator started on {self.host}:{self.port}")
            logger.info(f"📋 Device: {self.device_info['manufacturer']} {self.device_info['model']}")
            logger.info(f"🔢 Available registers: {len(self.register_map)} input, {len(self.coil_map)} coils, {len(self.discrete_input_map)} discrete inputs")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    logger.info(f"📡 Modbus TCP connection from {address}")
                    
                    # Handle client in a separate task
                    asyncio.create_task(self.handle_client(client_socket, address))
                    
                except Exception as e:
                    if self.running:
                        logger.error(f"Error accepting connection: {e}")
                        
        except Exception as e:
            logger.error(f"Failed to start Modbus TCP simulator: {e}")
        finally:
            await self.stop()
    
    async def handle_client(self, client_socket: socket.socket, address: tuple):
        """Handle Modbus TCP client connection"""
        try:
            while self.running:
                # Receive Modbus TCP request
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # Parse and process Modbus request
                response = await self.process_modbus_request(data)
                
                # Send response
                client_socket.send(response)
                
        except Exception as e:
            logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"📡 Modbus TCP connection closed: {address}")
    
    async def process_modbus_request(self, data: bytes) -> bytes:
        """Process Modbus TCP request and return response"""
        try:
            if len(data) < 8:  # Minimum Modbus TCP header size
                return self.create_error_response(0x01, 0x01)  # Illegal function
            
            # Parse Modbus TCP header
            transaction_id = struct.unpack('>H', data[0:2])[0]
            protocol_id = struct.unpack('>H', data[2:4])[0]
            length = struct.unpack('>H', data[4:6])[0]
            unit_id = data[6]
            function_code = data[7]
            
            # Validate protocol ID (should be 0 for Modbus TCP)
            if protocol_id != 0:
                return self.create_error_response(transaction_id, 0x01)
            
            # Process based on function code
            if function_code == 0x03:  # Read Holding Registers
                return await self.read_holding_registers(data, transaction_id)
            elif function_code == 0x04:  # Read Input Registers
                return await self.read_input_registers(data, transaction_id)
            elif function_code == 0x01:  # Read Coils
                return await self.read_coils(data, transaction_id)
            elif function_code == 0x02:  # Read Discrete Inputs
                return await self.read_discrete_inputs(data, transaction_id)
            elif function_code == 0x06:  # Write Single Register
                return await self.write_single_register(data, transaction_id)
            elif function_code == 0x05:  # Write Single Coil
                return await self.write_single_coil(data, transaction_id)
            else:
                return self.create_error_response(transaction_id, 0x01)  # Illegal function
                
        except Exception as e:
            logger.error(f"Error processing Modbus request: {e}")
            return self.create_error_response(0x00, 0x04)  # Slave device failure
    
    async def read_holding_registers(self, data: bytes, transaction_id: int) -> bytes:
        """Read holding registers (4x)"""
        try:
            start_address = struct.unpack('>H', data[8:10])[0]
            quantity = struct.unpack('>H', data[10:12])[0]
            
            # Validate address range
            if start_address < 40001 or start_address + quantity > 40007:
                return self.create_error_response(transaction_id, 0x02)  # Illegal data address
            
            # Read register values
            values = []
            for i in range(quantity):
                reg_addr = start_address + i
                if reg_addr in self.register_map:
                    reg_info = self.register_map[reg_addr]
                    if reg_info["type"] == "float":
                        # Convert float to 2 16-bit registers
                        float_val = reg_info["value"]
                        int_val = int(float_val * 100)  # Scale to preserve 2 decimal places
                        values.extend([(int_val >> 16) & 0xFFFF, int_val & 0xFFFF])
                    else:
                        values.append(int(reg_info["value"]))
                else:
                    values.append(0)
            
            # Create response
            byte_count = len(values) * 2
            response = struct.pack('>HHHBB', transaction_id, 0, byte_count + 3, self.device_info["unit_id"], 0x03)
            response += struct.pack('B', byte_count)
            
            for value in values:
                response += struct.pack('>H', value)
            
            return response
            
        except Exception as e:
            logger.error(f"Error reading holding registers: {e}")
            return self.create_error_response(transaction_id, 0x04)
    
    async def read_input_registers(self, data: bytes, transaction_id: int) -> bytes:
        """Read input registers (3x)"""
        try:
            start_address = struct.unpack('>H', data[8:10])[0]
            quantity = struct.unpack('>H', data[10:12])[0]
            
            # Validate address range
            if start_address < 30001 or start_address + quantity > 30009:
                return self.create_error_response(transaction_id, 0x02)  # Illegal data address
            
            # Read register values
            values = []
            for i in range(quantity):
                reg_addr = start_address + i
                if reg_addr in self.register_map:
                    reg_info = self.register_map[reg_addr]
                    if reg_info["type"] == "float":
                        # Convert float to 2 16-bit registers
                        float_val = reg_info["value"]
                        int_val = int(float_val * 100)  # Scale to preserve 2 decimal places
                        values.extend([(int_val >> 16) & 0xFFFF, int_val & 0xFFFF])
                    else:
                        values.append(int(reg_info["value"]))
                else:
                    values.append(0)
            
            # Create response
            byte_count = len(values) * 2
            response = struct.pack('>HHHBB', transaction_id, 0, byte_count + 3, self.device_info["unit_id"], 0x04)
            response += struct.pack('B', byte_count)
            
            for value in values:
                response += struct.pack('>H', value)
            
            return response
            
        except Exception as e:
            logger.error(f"Error reading input registers: {e}")
            return self.create_error_response(transaction_id, 0x04)
    
    async def read_coils(self, data: bytes, transaction_id: int) -> bytes:
        """Read coils (0x)"""
        try:
            start_address = struct.unpack('>H', data[8:10])[0]
            quantity = struct.unpack('>H', data[10:12])[0]
            
            # Validate address range
            if start_address < 1 or start_address + quantity > 6:
                return self.create_error_response(transaction_id, 0x02)  # Illegal data address
            
            # Read coil values
            coil_values = []
            for i in range(quantity):
                coil_addr = start_address + i
                if coil_addr in self.coil_map:
                    coil_values.append(self.coil_map[coil_addr]["value"])
                else:
                    coil_values.append(False)
            
            # Pack coil values into bytes
            byte_count = (quantity + 7) // 8
            response = struct.pack('>HHHBB', transaction_id, 0, byte_count + 3, self.device_info["unit_id"], 0x01)
            response += struct.pack('B', byte_count)
            
            # Pack coils into bytes
            coil_bytes = []
            for i in range(0, quantity, 8):
                byte_val = 0
                for j in range(8):
                    if i + j < quantity and coil_values[i + j]:
                        byte_val |= (1 << j)
                coil_bytes.append(byte_val)
            
            response += bytes(coil_bytes)
            return response
            
        except Exception as e:
            logger.error(f"Error reading coils: {e}")
            return self.create_error_response(transaction_id, 0x04)
    
    async def read_discrete_inputs(self, data: bytes, transaction_id: int) -> bytes:
        """Read discrete inputs (1x)"""
        try:
            start_address = struct.unpack('>H', data[8:10])[0]
            quantity = struct.unpack('>H', data[10:12])[0]
            
            # Validate address range
            if start_address < 10001 or start_address + quantity > 10006:
                return self.create_error_response(transaction_id, 0x02)  # Illegal data address
            
            # Read discrete input values
            input_values = []
            for i in range(quantity):
                input_addr = start_address + i
                if input_addr in self.discrete_input_map:
                    input_values.append(self.discrete_input_map[input_addr]["value"])
                else:
                    input_values.append(False)
            
            # Pack input values into bytes
            byte_count = (quantity + 7) // 8
            response = struct.pack('>HHHBB', transaction_id, 0, byte_count + 3, self.device_info["unit_id"], 0x02)
            response += struct.pack('B', byte_count)
            
            # Pack inputs into bytes
            input_bytes = []
            for i in range(0, quantity, 8):
                byte_val = 0
                for j in range(8):
                    if i + j < quantity and input_values[i + j]:
                        byte_val |= (1 << j)
                input_bytes.append(byte_val)
            
            response += bytes(input_bytes)
            return response
            
        except Exception as e:
            logger.error(f"Error reading discrete inputs: {e}")
            return self.create_error_response(transaction_id, 0x04)
    
    async def write_single_register(self, data: bytes, transaction_id: int) -> bytes:
        """Write single holding register"""
        try:
            address = struct.unpack('>H', data[8:10])[0]
            value = struct.unpack('>H', data[10:12])[0]
            
            # Validate address
            if address not in self.register_map:
                return self.create_error_response(transaction_id, 0x02)  # Illegal data address
            
            # Update register value
            reg_info = self.register_map[address]
            if reg_info["type"] == "float":
                # Convert from 16-bit to float (assuming scaled by 100)
                reg_info["value"] = value / 100.0
            else:
                reg_info["value"] = value
            
            logger.info(f"📝 Updated register {address} ({reg_info['name']}) to {reg_info['value']} {reg_info['unit']}")
            
            # Echo back the request
            return data
            
        except Exception as e:
            logger.error(f"Error writing register: {e}")
            return self.create_error_response(transaction_id, 0x04)
    
    async def write_single_coil(self, data: bytes, transaction_id: int) -> bytes:
        """Write single coil"""
        try:
            address = struct.unpack('>H', data[8:10])[0]
            value = struct.unpack('>H', data[10:12])[0]
            
            # Validate address
            if address not in self.coil_map:
                return self.create_error_response(transaction_id, 0x02)  # Illegal data address
            
            # Update coil value
            coil_value = value == 0xFF00  # Modbus coil write convention
            self.coil_map[address]["value"] = coil_value
            
            logger.info(f"📝 Updated coil {address} ({self.coil_map[address]['name']}) to {coil_value}")
            
            # Echo back the request
            return data
            
        except Exception as e:
            logger.error(f"Error writing coil: {e}")
            return self.create_error_response(transaction_id, 0x04)
    
    def create_error_response(self, transaction_id: int, error_code: int) -> bytes:
        """Create Modbus error response"""
        return struct.pack('>HHHBB', transaction_id, 0, 3, self.device_info["unit_id"], error_code | 0x80)
    
    async def simulate_data_changes(self):
        """Simulate realistic data changes"""
        while self.running:
            try:
                # Simulate temperature variations
                if 30001 in self.register_map:
                    temp1 = self.register_map[30001]["value"]
                    temp1 += random.uniform(-0.5, 0.5)
                    temp1 = max(18.0, min(28.0, temp1))  # Keep in realistic range
                    self.register_map[30001]["value"] = round(temp1, 1)
                
                if 30002 in self.register_map:
                    temp2 = self.register_map[30002]["value"]
                    temp2 += random.uniform(-0.3, 0.3)
                    temp2 = max(19.0, min(27.0, temp2))
                    self.register_map[30002]["value"] = round(temp2, 1)
                
                # Simulate pressure variations
                if 30003 in self.register_map:
                    pressure = self.register_map[30003]["value"]
                    pressure += random.uniform(-0.1, 0.1)
                    pressure = max(1.5, min(4.0, pressure))
                    self.register_map[30003]["value"] = round(pressure, 1)
                
                # Simulate flow rate variations
                if 30004 in self.register_map:
                    flow = self.register_map[30004]["value"]
                    flow += random.uniform(-2.0, 2.0)
                    flow = max(30.0, min(60.0, flow))
                    self.register_map[30004]["value"] = round(flow, 1)
                
                # Simulate motor speed variations
                if 30006 in self.register_map:
                    speed = self.register_map[30006]["value"]
                    speed += random.uniform(-50, 50)
                    speed = max(1400, min(1500, speed))
                    self.register_map[30006]["value"] = int(speed)
                
                await asyncio.sleep(2)  # Update every 2 seconds
                
            except Exception as e:
                logger.error(f"Error in data simulation: {e}")
                await asyncio.sleep(5)
    
    async def stop(self):
        """Stop the Modbus TCP simulator"""
        self.running = False
        if self.socket:
            self.socket.close()
        logger.info("🔧 Modbus TCP Simulator stopped")
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get device information for documentation"""
        return {
            "device_info": self.device_info,
            "register_map": self.register_map,
            "coil_map": self.coil_map,
            "discrete_input_map": self.discrete_input_map,
            "error_codes": self.error_codes,
            "troubleshooting": self.troubleshooting
        }


async def main():
    """Main function to run the Modbus TCP simulator"""
    simulator = ModbusTCPSimulator()
    
    try:
        # Start data simulation task
        simulation_task = asyncio.create_task(simulator.simulate_data_changes())
        
        # Start the simulator
        await simulator.start()
        
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down Modbus TCP Simulator...")
    finally:
        await simulator.stop()


if __name__ == "__main__":
    asyncio.run(main())
