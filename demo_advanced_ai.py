"""
Demo: Advanced AI Features for Industrial Gateway
Shows sophisticated AI capabilities that go beyond basic protocol handling
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def demo_advanced_ai():
    """Demonstrate advanced AI features for industrial gateway"""
    print("🧠 Advanced AI Features Demo - Industrial Gateway")
    print("=" * 70)
    print("Sophisticated AI capabilities that transform your gateway into an intelligent system!")
    print()
    
    # Import the advanced AI features
    from ai.advanced_ai_features import AdvancedAIFeatures
    
    # Initialize the advanced AI engine
    print("🚀 Step 1: Initializing Advanced AI Engine")
    print("   Loading sophisticated AI models...")
    
    ai_engine = AdvancedAIFeatures()
    print("   ✅ Advanced AI engine initialized")
    print()
    
    # Test 1: Intelligent Protocol Selection
    print("🎯 Step 2: Intelligent Protocol Selection")
    print("   AI analyzes device characteristics and query intent...")
    print()
    
    device_info = {
        "manufacturer": "Honeywell",
        "model": "T6 Pro Thermostat",
        "device_type": "thermostat",
        "network_info": {
            "ip": "192.168.1.100",
            "port": 80,
            "protocol": "HTTP",
            "response_time": 50
        },
        "capabilities": ["temperature_control", "scheduling", "remote_access"],
        "security_features": ["encryption", "authentication"]
    }
    
    query = "I need to optimize the HVAC system for energy efficiency while maintaining comfort"
    
    print(f"   Device: {device_info['manufacturer']} {device_info['model']}")
    print(f"   Query: \"{query}\"")
    print("   🤖 AI Analysis...")
    
    result = await ai_engine.intelligent_protocol_selection(device_info, query)
    
    if result["success"]:
        rec = result["protocol_recommendation"]
        print(f"   ✅ Recommended Protocol: {rec['recommended_protocol']}")
        print(f"   🎯 Confidence: {rec['confidence']}")
        print(f"   💡 Reasoning: {rec['reasoning']}")
        print(f"   🔄 Alternatives: {', '.join(rec['alternative_approaches'])}")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print()
    
    # Test 2: Predictive Maintenance Analysis
    print("🔮 Step 3: Predictive Maintenance Analysis")
    print("   AI analyzes device data to predict potential failures...")
    print()
    
    device_data = [
        {"timestamp": "2024-01-01T10:00:00", "temperature": 72, "error": False},
        {"timestamp": "2024-01-01T11:00:00", "temperature": 73, "error": False},
        {"timestamp": "2024-01-01T12:00:00", "temperature": 75, "error": False},
        {"timestamp": "2024-01-01T13:00:00", "temperature": 78, "error": True},
        {"timestamp": "2024-01-01T14:00:00", "temperature": 80, "error": True},
        {"timestamp": "2024-01-01T15:00:00", "temperature": 82, "error": True},
        {"timestamp": "2024-01-01T16:00:00", "temperature": 85, "error": True},
        {"timestamp": "2024-01-01T17:00:00", "temperature": 88, "error": True}
    ]
    
    print(f"   📊 Analyzing {len(device_data)} data points...")
    print("   🤖 AI Analysis...")
    
    result = await ai_engine.predictive_maintenance_analysis(device_data)
    
    if result["success"]:
        analysis = result["maintenance_analysis"]
        print(f"   ⚠️  Risk Level: {analysis['risk_level']}")
        print(f"   📈 Failure Probability: {analysis['failure_probability']}")
        print(f"   📅 Predicted Failure: {analysis['predicted_failure_date']}")
        print(f"   🎯 Confidence: {analysis['confidence']}")
        print(f"   💡 Explanation: {analysis['explanation']}")
        print(f"   🔧 Recommended Actions: {len(analysis['recommended_actions'])} actions")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print()
    
    # Test 3: Energy Optimization
    print("⚡ Step 4: Intelligent Energy Optimization")
    print("   AI analyzes building data to recommend energy savings...")
    print()
    
    building_data = {
        "hvac": {
            "current_usage": 1500,  # kWh
            "efficiency": 0.75,
            "schedule": "24/7",
            "temperature_setpoint": 72
        },
        "lighting": {
            "current_usage": 800,  # kWh
            "efficiency": 0.60,
            "occupancy_sensors": False,
            "smart_controls": False
        },
        "equipment": {
            "current_usage": 1200,  # kWh
            "efficiency": 0.80,
            "load_balancing": False
        },
        "occupancy": {
            "peak_hours": "9AM-5PM",
            "weekend_usage": 0.3,
            "vacation_periods": ["Dec 25-31"]
        },
        "weather": {
            "current_temp": 75,
            "season": "summer",
            "humidity": 60
        }
    }
    
    print("   🏢 Building Data Analysis...")
    print("   🤖 AI Optimization...")
    
    result = await ai_engine.intelligent_energy_optimization(building_data)
    
    if result["success"]:
        opt = result["energy_optimization"]
        savings = opt["total_potential_savings"]
        print(f"   💰 Potential Savings: {savings['energy_kwh']} kWh ({savings['energy_percentage']}%)")
        print(f"   💵 Cost Savings: ${savings['cost_dollars']}")
        print(f"   📋 Recommendations: {len(opt['recommendations'])} optimization strategies")
        print(f"   📅 Implementation Plan: {len(opt['implementation_plan'])} steps")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print()
    
    # Test 4: Natural Language Automation
    print("🗣️  Step 5: Natural Language Automation")
    print("   AI processes complex automation requests...")
    print()
    
    user_request = "When the building is empty after 6 PM, automatically lower the temperature to 68°F, dim the lights to 30%, and activate security mode. But if someone enters, immediately restore comfort settings and notify security."
    
    system_context = {
        "available_systems": ["hvac", "lighting", "security", "occupancy"],
        "current_occupancy": "empty",
        "time": "18:30",
        "security_status": "normal"
    }
    
    print(f"   📝 Request: \"{user_request[:80]}...\"")
    print("   🤖 AI Processing...")
    
    result = await ai_engine.natural_language_automation(user_request, system_context)
    
    if result["success"]:
        plan = result["automation_plan"]
        print(f"   📋 Automation Plan: {plan['automation_plan']['title']}")
        print(f"   ⏱️  Duration: {plan['automation_plan']['estimated_duration']}")
        print(f"   🔧 Steps: {len(plan['automation_plan']['steps'])} actions")
        print(f"   🛡️  Safety Considerations: {len(plan['safety_considerations'])} items")
        print(f"   📊 Monitoring: {len(plan['monitoring_plan'])} metrics")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print()
    
    # Test 5: Anomaly Detection
    print("🚨 Step 6: Real-time Anomaly Detection")
    print("   AI monitors for unusual patterns and potential issues...")
    print()
    
    real_time_data = [
        {"timestamp": "2024-01-01T10:00:00", "temperature": 72, "humidity": 45, "error": False},
        {"timestamp": "2024-01-01T10:05:00", "temperature": 73, "humidity": 46, "error": False},
        {"timestamp": "2024-01-01T10:10:00", "temperature": 75, "humidity": 48, "error": False},
        {"timestamp": "2024-01-01T10:15:00", "temperature": 78, "humidity": 52, "error": False},
        {"timestamp": "2024-01-01T10:20:00", "temperature": 82, "humidity": 58, "error": False},
        {"timestamp": "2024-01-01T10:25:00", "temperature": 87, "humidity": 65, "error": True},
        {"timestamp": "2024-01-01T10:30:00", "temperature": 92, "humidity": 72, "error": True}
    ]
    
    print(f"   📊 Monitoring {len(real_time_data)} real-time data points...")
    print("   🤖 AI Anomaly Detection...")
    
    result = await ai_engine.anomaly_detection_and_alerting(real_time_data)
    
    if result["success"]:
        analysis = result["anomaly_analysis"]
        print(f"   ⚠️  Overall Risk: {analysis['overall_risk_level']}")
        print(f"   🚨 Anomalies Detected: {len(analysis['anomalies_detected'])}")
        
        for anomaly in analysis["anomalies_detected"]:
            print(f"      • {anomaly['type']}: {anomaly['severity']} severity")
            print(f"        {anomaly['description']}")
            print(f"        Confidence: {anomaly['confidence']}")
        
        print(f"   🔧 Immediate Actions: {len(analysis['immediate_actions'])}")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print()
    
    # Summary
    print("🎯 Advanced AI Demo Complete!")
    print("   Your industrial gateway now has:")
    print("   • 🧠 Intelligent protocol selection")
    print("   • 🔮 Predictive maintenance analysis")
    print("   • ⚡ Energy optimization recommendations")
    print("   • 🗣️  Natural language automation")
    print("   • 🚨 Real-time anomaly detection")
    print()
    print("   🚀 This transforms your gateway from a simple protocol converter")
    print("      into an intelligent industrial automation system!")
    print()
    print("   💡 Perfect for:")
    print("      • Smart buildings and facilities")
    print("      • Industrial IoT applications")
    print("      • Energy management systems")
    print("      • Predictive maintenance programs")
    print("      • Automated building control")


if __name__ == "__main__":
    asyncio.run(demo_advanced_ai())
