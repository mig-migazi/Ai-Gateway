"""
Advanced AI Features for Industrial Gateway
Sophisticated AI capabilities that go beyond basic protocol handling
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import openai
from core.config import config

logger = logging.getLogger(__name__)


class AdvancedAIFeatures:
    """
    Advanced AI features for industrial gateway
    Uses OpenAI API for sophisticated analysis and automation
    """
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=config.openai_api_key)
        self.conversation_history = []
        self.device_behavior_patterns = {}
        self.anomaly_detection_history = []
    
    async def intelligent_protocol_selection(self, device_info: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        AI-powered protocol selection based on device characteristics and query intent
        Goes beyond simple port-based detection
        """
        try:
            prompt = f"""
            You are an industrial automation expert. Analyze this device and query to recommend the best protocol approach.
            
            Device Info: {json.dumps(device_info, indent=2)}
            User Query: "{query}"
            
            Available Protocols: REST, BACnet IP, Modbus TCP, OPC-UA
            
            Consider:
            - Device type and manufacturer
            - Network characteristics
            - Query complexity and real-time requirements
            - Security implications
            - Performance optimization
            
            Respond with JSON:
            {{
                "recommended_protocol": "protocol_name",
                "confidence": 0.95,
                "reasoning": "detailed explanation",
                "alternative_approaches": ["protocol1", "protocol2"],
                "optimization_suggestions": ["suggestion1", "suggestion2"]
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=config.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "protocol_recommendation": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in intelligent protocol selection: {e}")
            return {"success": False, "error": str(e)}
    
    async def predictive_maintenance_analysis(self, device_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        AI-powered predictive maintenance analysis
        Analyzes device data patterns to predict failures
        """
        try:
            # Prepare data for analysis
            data_summary = self._prepare_maintenance_data(device_data)
            
            prompt = f"""
            You are a predictive maintenance AI expert. Analyze this industrial device data to predict potential failures.
            
            Device Data Summary: {json.dumps(data_summary, indent=2)}
            
            Analyze for:
            - Temperature trends and anomalies
            - Vibration patterns
            - Performance degradation
            - Error frequency
            - Usage patterns
            
            Provide:
            1. Risk assessment (Low/Medium/High)
            2. Predicted failure timeline
            3. Recommended maintenance actions
            4. Cost-benefit analysis
            5. Specific metrics to monitor
            
            Respond with JSON:
            {{
                "risk_level": "High/Medium/Low",
                "failure_probability": 0.85,
                "predicted_failure_date": "2024-01-15",
                "confidence": 0.78,
                "recommended_actions": [
                    {{"action": "replace_filter", "priority": "high", "cost": "$50"}},
                    {{"action": "calibrate_sensors", "priority": "medium", "cost": "$200"}}
                ],
                "monitoring_metrics": ["temperature", "vibration", "error_rate"],
                "explanation": "detailed analysis explanation"
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=config.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "maintenance_analysis": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in predictive maintenance analysis: {e}")
            return {"success": False, "error": str(e)}
    
    async def intelligent_energy_optimization(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered energy optimization for smart buildings
        Analyzes HVAC, lighting, and equipment usage patterns
        """
        try:
            prompt = f"""
            You are an energy optimization AI expert. Analyze this building data to recommend energy savings.
            
            Building Data: {json.dumps(building_data, indent=2)}
            
            Consider:
            - HVAC efficiency and scheduling
            - Lighting optimization
            - Equipment usage patterns
            - Occupancy patterns
            - Weather conditions
            - Energy pricing
            - Comfort requirements
            
            Provide optimization recommendations with:
            - Potential energy savings (kWh and %)
            - Cost savings ($)
            - Implementation complexity
            - Payback period
            - Comfort impact
            
            Respond with JSON:
            {{
                "total_potential_savings": {{
                    "energy_kwh": 1500,
                    "energy_percentage": 25,
                    "cost_dollars": 300
                }},
                "recommendations": [
                    {{
                        "category": "HVAC",
                        "action": "optimize_schedule",
                        "savings_kwh": 800,
                        "savings_dollars": 160,
                        "implementation": "easy",
                        "payback_months": 6
                    }}
                ],
                "implementation_plan": [
                    {{"step": 1, "action": "update_hvac_schedule", "timeline": "1 week"}},
                    {{"step": 2, "action": "install_smart_thermostats", "timeline": "2 weeks"}}
                ],
                "monitoring_metrics": ["energy_usage", "cost", "comfort_score"]
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=config.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "energy_optimization": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in energy optimization: {e}")
            return {"success": False, "error": str(e)}
    
    async def natural_language_automation(self, user_request: str, system_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advanced natural language processing for complex automation requests
        Understands complex, multi-step automation scenarios
        """
        try:
            prompt = f"""
            You are an industrial automation AI assistant. Process this complex user request and create an automation plan.
            
            User Request: "{user_request}"
            System Context: {json.dumps(system_context, indent=2)}
            
            Available Systems:
            - HVAC (temperature, humidity, airflow)
            - Lighting (brightness, scheduling, occupancy)
            - Security (access control, cameras, alarms)
            - Energy (monitoring, optimization, billing)
            - Equipment (status, maintenance, control)
            
            Create a detailed automation plan that:
            1. Breaks down the request into actionable steps
            2. Identifies required protocols and devices
            3. Considers safety and efficiency
            4. Provides fallback options
            5. Includes monitoring and validation
            
            Respond with JSON:
            {{
                "automation_plan": {{
                    "title": "Plan title",
                    "description": "Detailed description",
                    "steps": [
                        {{
                            "step": 1,
                            "action": "check_temperature",
                            "protocol": "BACnet",
                            "device": "thermostat_101",
                            "expected_result": "temperature_reading",
                            "validation": "temperature_within_range"
                        }}
                    ],
                    "estimated_duration": "5 minutes",
                    "success_criteria": ["criteria1", "criteria2"],
                    "fallback_actions": ["fallback1", "fallback2"]
                }},
                "required_devices": ["device1", "device2"],
                "required_protocols": ["BACnet", "REST"],
                "safety_considerations": ["consideration1", "consideration2"],
                "monitoring_plan": ["metric1", "metric2"]
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=config.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=1200
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "automation_plan": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in natural language automation: {e}")
            return {"success": False, "error": str(e)}
    
    async def anomaly_detection_and_alerting(self, real_time_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        AI-powered anomaly detection for real-time monitoring
        Identifies unusual patterns and potential issues
        """
        try:
            # Analyze data for anomalies
            data_analysis = self._analyze_data_patterns(real_time_data)
            
            prompt = f"""
            You are an anomaly detection AI expert. Analyze this real-time industrial data for anomalies.
            
            Data Analysis: {json.dumps(data_analysis, indent=2)}
            
            Look for:
            - Statistical anomalies (outliers, trends)
            - Pattern deviations
            - Performance degradation
            - Security threats
            - Equipment malfunctions
            - Environmental changes
            
            Provide:
            1. Anomaly severity (Critical/High/Medium/Low)
            2. Affected systems
            3. Potential causes
            4. Recommended actions
            5. Alert priority
            
            Respond with JSON:
            {{
                "anomalies_detected": [
                    {{
                        "type": "temperature_spike",
                        "severity": "High",
                        "affected_device": "hvac_unit_101",
                        "description": "Temperature increased 15°F in 5 minutes",
                        "potential_cause": "sensor_malfunction_or_equipment_failure",
                        "recommended_action": "immediate_inspection",
                        "alert_priority": 1,
                        "confidence": 0.92
                    }}
                ],
                "overall_risk_level": "High",
                "immediate_actions": ["action1", "action2"],
                "monitoring_recommendations": ["metric1", "metric2"]
            }}
            """
            
            response = await self.client.chat.completions.create(
                model=config.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "anomaly_analysis": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            return {"success": False, "error": str(e)}
    
    def _prepare_maintenance_data(self, device_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare device data for maintenance analysis"""
        if not device_data:
            return {"error": "No data provided"}
        
        # Calculate basic statistics
        temperatures = [d.get("temperature", 0) for d in device_data if "temperature" in d]
        errors = [d for d in device_data if d.get("error", False)]
        
        return {
            "data_points": len(device_data),
            "temperature_stats": {
                "min": min(temperatures) if temperatures else 0,
                "max": max(temperatures) if temperatures else 0,
                "avg": sum(temperatures) / len(temperatures) if temperatures else 0
            },
            "error_count": len(errors),
            "error_rate": len(errors) / len(device_data) if device_data else 0,
            "time_range": {
                "start": device_data[0].get("timestamp", ""),
                "end": device_data[-1].get("timestamp", "")
            }
        }
    
    def _analyze_data_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze data patterns for anomaly detection"""
        if not data:
            return {"error": "No data provided"}
        
        # Basic pattern analysis
        recent_data = data[-10:] if len(data) >= 10 else data
        
        return {
            "data_points": len(data),
            "recent_trends": {
                "temperature_trend": "increasing" if len(recent_data) > 1 else "stable",
                "error_frequency": len([d for d in recent_data if d.get("error", False)]),
                "performance_score": 85  # Mock calculation
            },
            "statistical_summary": {
                "mean_temperature": sum(d.get("temperature", 0) for d in data) / len(data),
                "variance": 0.5,  # Mock calculation
                "outliers": 2  # Mock calculation
            }
        }
