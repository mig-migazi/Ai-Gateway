"""
Configuration management for the AI Gateway
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


class GatewayConfig(BaseSettings):
    """Configuration settings for the AI Gateway"""
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    
    # Gateway Configuration
    gateway_host: str = Field(default="0.0.0.0", env="GATEWAY_HOST")
    gateway_port: int = Field(default=8000, env="GATEWAY_PORT")
    
    # MCP Server Configuration
    mcp_server_host: str = Field(default="localhost", env="MCP_SERVER_HOST")
    mcp_server_port: int = Field(default=3000, env="MCP_SERVER_PORT")
    
    # Protocol Configuration
    bacnet_ip_port: int = Field(default=47808, env="BACNET_IP_PORT")
    modbus_tcp_port: int = Field(default=502, env="MODBUS_TCP_PORT")
    opc_ua_port: int = Field(default=4840, env="OPC_UA_PORT")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/gateway.log", env="LOG_FILE")
    
    # Device Discovery Configuration
    discovery_timeout: int = Field(default=10, env="DISCOVERY_TIMEOUT")
    max_discovery_attempts: int = Field(default=3, env="MAX_DISCOVERY_ATTEMPTS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_config() -> GatewayConfig:
    """Load configuration from environment variables and .env file"""
    # Load .env file if it exists
    if os.path.exists(".env"):
        load_dotenv()
    
    try:
        return GatewayConfig()
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print("Please ensure you have a .env file with the required configuration.")
        print("Copy env.example to .env and fill in your OpenAI API key.")
        raise


# Global configuration instance
config = load_config()
