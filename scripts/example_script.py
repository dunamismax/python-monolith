#!/usr/bin/env python3
"""
Example script demonstrating the use of shared utilities.

This script shows how to use the shared utilities module for common tasks
like logging, configuration management, and file operations.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.utils import (
    setup_logging,
    Timer,
    ConfigManager,
    get_environment_info,
    get_file_hash,
    ensure_directory
)


def main():
    """Main function demonstrating shared utilities."""
    # Setup logging
    logger = setup_logging(level="INFO")
    logger.info("Starting example script")
    
    # Demonstrate timer
    with Timer() as timer:
        logger.info("Performing some work...")
        
        # Get environment info
        env_info = get_environment_info()
        logger.info(f"Running on platform: {env_info['platform']}")
        logger.info(f"Project root: {env_info['project_root']}")
        
        # Create a temporary directory
        temp_dir = ensure_directory("temp")
        logger.info(f"Created directory: {temp_dir}")
        
        # Demonstrate configuration management
        config = ConfigManager(temp_dir / "example_config.json")
        config.set("app.name", "Python Monolith")
        config.set("app.version", "0.1.0")
        config.set("database.host", "localhost")
        config.set("database.port", 5432)
        config.save()
        
        logger.info(f"App name: {config.get('app.name')}")
        logger.info(f"Database config: {config.get('database.host')}:{config.get('database.port')}")
        
        # Calculate hash of this script file
        script_hash = get_file_hash(__file__)
        logger.info(f"Script hash (SHA256): {script_hash}")
    
    logger.info(f"Script completed in {timer.elapsed_time:.3f} seconds")


if __name__ == "__main__":
    main()