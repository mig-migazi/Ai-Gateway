"""
Main entry point for the AI Gateway
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.mcp_server import main as mcp_main
from src.core.config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point"""
    logger.info("Starting AI Gateway...")
    logger.info(f"Configuration loaded from: {config.env_file}")
    
    try:
        # Start the MCP server
        await mcp_main()
    except KeyboardInterrupt:
        logger.info("Shutting down AI Gateway...")
    except Exception as e:
        logger.error(f"Error starting AI Gateway: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
