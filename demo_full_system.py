"""
Full System Demo - AI Gateway with Real-time Data Streaming
Demonstrates the complete system: simulators, MCP server, and dashboard
"""

import asyncio
import subprocess
import time
import sys
from pathlib import Path

def print_banner():
    """Print demo banner"""
    print("=" * 80)
    print("🤖 AI GATEWAY FULL SYSTEM DEMO")
    print("=" * 80)
    print("Real-time Industrial Protocol Intelligence & Data Flow Visualization")
    print("=" * 80)
    print()

def print_section(title):
    """Print section header"""
    print(f"\n🚀 {title}")
    print("-" * 60)

def run_command(command, description, background=False):
    """Run a command and return the process"""
    print(f"   {description}...")
    try:
        if background:
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            print(f"   ✅ {description} started (PID: {process.pid})")
            return process
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ {description} completed")
                return result.stdout
            else:
                print(f"   ❌ {description} failed: {result.stderr}")
                return None
    except Exception as e:
        print(f"   ❌ {description} error: {e}")
        return None

async def demo_full_system():
    """Demonstrate the complete AI Gateway system"""
    print_banner()
    
    # Step 1: Start REST Simulator
    print_section("Starting REST API Simulator")
    rest_process = run_command(
        "cd /Users/miguel/Projects/AIGateway && source venv/bin/activate && python simulators/rest_simulator.py",
        "REST API Simulator",
        background=True
    )
    
    if not rest_process:
        print("❌ Failed to start REST simulator. Exiting.")
        return
    
    # Wait for simulator to start
    print("   ⏳ Waiting for REST simulator to initialize...")
    await asyncio.sleep(3)
    
    # Step 2: Start Dashboard Server
    print_section("Starting Dashboard Server")
    dashboard_process = run_command(
        "cd /Users/miguel/Projects/AIGateway && source venv/bin/activate && python dashboard_server.py",
        "Dashboard Server",
        background=True
    )
    
    if not dashboard_process:
        print("❌ Failed to start dashboard server. Exiting.")
        return
    
    # Wait for dashboard to start
    print("   ⏳ Waiting for dashboard server to initialize...")
    await asyncio.sleep(3)
    
    # Step 3: Test REST API
    print_section("Testing REST API Endpoints")
    
    # Test basic endpoints
    test_commands = [
        ("curl -s http://localhost:8000/api/temperature", "Temperature endpoint"),
        ("curl -s http://localhost:8000/api/humidity", "Humidity endpoint"),
        ("curl -s http://localhost:8000/api/stream/status", "Stream status"),
        ("curl -s http://localhost:8000/api/analytics", "Analytics endpoint")
    ]
    
    for command, description in test_commands:
        result = run_command(command, description)
        if result:
            try:
                import json
                data = json.loads(result)
                print(f"      📊 {description}: {data}")
            except:
                print(f"      📊 {description}: {result[:100]}...")
    
    # Step 4: Test Dashboard API
    print_section("Testing Dashboard API")
    
    dashboard_commands = [
        ("curl -s http://localhost:8080/api/mcp/status", "MCP Status"),
        ("curl -s http://localhost:8080/api/analytics", "Dashboard Analytics")
    ]
    
    for command, description in dashboard_commands:
        result = run_command(command, description)
        if result:
            try:
                import json
                data = json.loads(result)
                print(f"      📊 {description}: {data}")
            except:
                print(f"      📊 {description}: {result[:100]}...")
    
    # Step 5: Simulate MCP Activity
    print_section("Simulating MCP Activity")
    
    # Simulate some MCP connections and decisions
    mcp_commands = [
        ("curl -s -X POST http://localhost:8080/api/mcp/simulate", "Simulate MCP Connection"),
        ("curl -s -X POST -H 'Content-Type: application/json' -d '{\"query\":\"What is the temperature?\"}' http://localhost:8080/api/mcp/query", "Simulate AI Query"),
        ("curl -s -X POST -H 'Content-Type: application/json' -d '{\"query\":\"Optimize energy usage\"}' http://localhost:8080/api/mcp/query", "Simulate Energy Query")
    ]
    
    for command, description in mcp_commands:
        result = run_command(command, description)
        if result:
            try:
                import json
                data = json.loads(result)
                print(f"      🧠 {description}: {data.get('message', 'Success')}")
            except:
                print(f"      🧠 {description}: {result[:100]}...")
    
    # Step 6: Show System Status
    print_section("System Status Summary")
    
    print("   🌐 REST Simulator: http://localhost:8000")
    print("      • Real-time data streaming")
    print("      • Sensor endpoints (temperature, humidity, pressure)")
    print("      • Analytics and history")
    print()
    
    print("   📊 Dashboard: http://localhost:8080")
    print("      • Real-time data visualization")
    print("      • AI decision tracking")
    print("      • System activity monitoring")
    print()
    
    print("   🧠 MCP Server: Ready for integration")
    print("      • Dynamic protocol implementation")
    print("      • Local AI processing")
    print("      • Protocol knowledge base")
    print()
    
    # Step 7: Interactive Demo
    print_section("Interactive Demo Instructions")
    print("   🎯 Open your browser and go to: http://localhost:8080")
    print("   📈 Watch real-time data streaming from the REST simulator")
    print("   🧠 See AI decisions being made in real-time")
    print("   📊 Monitor system activity and performance")
    print()
    print("   🔧 Test the system:")
    print("      • Click 'Start Stream' to begin data streaming")
    print("      • Click 'Test AI Query' to simulate MCP queries")
    print("      • Watch the charts update with real-time data")
    print("      • Monitor AI decisions in the decision panel")
    print()
    
    # Step 8: Keep system running
    print_section("System Running")
    print("   ✅ All systems are now running!")
    print("   🌐 Dashboard: http://localhost:8080")
    print("   🔌 REST API: http://localhost:8000")
    print("   📚 API Docs: http://localhost:8000/docs")
    print()
    print("   Press Ctrl+C to stop all services...")
    print()
    
    try:
        # Keep the demo running
        while True:
            await asyncio.sleep(10)
            print(f"   ⏰ System running... {time.strftime('%H:%M:%S')}")
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        
        # Stop processes
        if rest_process:
            rest_process.terminate()
            print("   ✅ REST Simulator stopped")
        
        if dashboard_process:
            dashboard_process.terminate()
            print("   ✅ Dashboard Server stopped")
        
        print("   🎯 Demo completed successfully!")

if __name__ == "__main__":
    try:
        asyncio.run(demo_full_system())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        sys.exit(1)
