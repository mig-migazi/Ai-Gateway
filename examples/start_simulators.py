"""
Start Simulators - Start all protocol simulators for testing
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

def start_rest_simulator():
    """Start the REST API simulator"""
    print("Starting REST API Simulator...")
    try:
        process = subprocess.Popen([
            sys.executable, "simulators/rest_simulator.py"
        ], cwd=Path(__file__).parent.parent)
        print(f"REST simulator started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"Failed to start REST simulator: {e}")
        return None

def start_bacnet_simulator():
    """Start the BACnet IP simulator"""
    print("Starting BACnet IP Simulator...")
    try:
        process = subprocess.Popen([
            sys.executable, "simulators/bacnet_simulator.py"
        ], cwd=Path(__file__).parent.parent)
        print(f"BACnet simulator started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"Failed to start BACnet simulator: {e}")
        return None

def main():
    """Start all simulators"""
    print("AI Gateway Simulators")
    print("=" * 30)
    
    processes = []
    
    # Start REST simulator
    rest_process = start_rest_simulator()
    if rest_process:
        processes.append(rest_process)
    
    # Wait a moment
    time.sleep(2)
    
    # Start BACnet simulator
    bacnet_process = start_bacnet_simulator()
    if bacnet_process:
        processes.append(bacnet_process)
    
    if processes:
        print(f"\nStarted {len(processes)} simulators")
        print("Press Ctrl+C to stop all simulators")
        
        try:
            # Wait for all processes
            for process in processes:
                process.wait()
        except KeyboardInterrupt:
            print("\nStopping simulators...")
            for process in processes:
                process.terminate()
                process.wait()
            print("All simulators stopped")
    else:
        print("No simulators started")

if __name__ == "__main__":
    main()
