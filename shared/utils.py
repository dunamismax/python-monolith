"""
Shared utilities for the Python Monolith repository.

This module contains common functions and classes that can be used
across different applications in the monolith.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union
import hashlib


def get_project_root() -> Path:
    """
    Get the root directory of the Python Monolith project.
    
    Returns:
        Path: The project root directory
    """
    return Path(__file__).parent.parent


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for applications.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        format_string: Custom format string for log messages
    
    Returns:
        logging.Logger: Configured logger instance
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure basic logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[
            logging.StreamHandler(),
            *([] if log_file is None else [logging.FileHandler(log_file)])
        ]
    )
    
    return logging.getLogger("python-monolith")


def load_json_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the JSON configuration file
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    
    Raises:
        FileNotFoundError: If the config file doesn't exist
        json.JSONDecodeError: If the JSON is invalid
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_config(config: Dict[str, Any], config_path: Union[str, Path]) -> None:
    """
    Save configuration to a JSON file.
    
    Args:
        config: Configuration dictionary to save
        config_path: Path where to save the JSON file
    """
    config_path = Path(config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_file_hash(file_path: Union[str, Path], algorithm: str = "sha256") -> str:
    """
    Calculate hash of a file.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (md5, sha1, sha256, etc.)
    
    Returns:
        str: Hexadecimal hash digest
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the algorithm is not supported
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        hash_obj = hashlib.new(algorithm)
    except ValueError:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def ensure_directory(directory_path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it and parent directories if necessary.
    
    Args:
        directory_path: Path to the directory
    
    Returns:
        Path: The directory path as a Path object
    """
    directory_path = Path(directory_path)
    directory_path.mkdir(parents=True, exist_ok=True)
    return directory_path


def get_environment_info() -> Dict[str, Any]:
    """
    Get information about the current environment.
    
    Returns:
        Dict[str, Any]: Environment information
    """
    return {
        "python_version": os.sys.version,
        "platform": os.sys.platform,
        "cwd": str(Path.cwd()),
        "project_root": str(get_project_root()),
        "timestamp": datetime.now().isoformat(),
        "env_vars": {
            key: value for key, value in os.environ.items()
            if not key.startswith(('SECRET', 'PASSWORD', 'TOKEN', 'KEY'))
        }
    }


class Timer:
    """
    A simple context manager for timing code execution.
    
    Usage:
        with Timer() as t:
            # some code
            pass
        print(f"Execution took {t.elapsed_time:.2f} seconds")
    """
    
    def __init__(self) -> None:
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
    
    def __enter__(self) -> 'Timer':
        self.start_time = datetime.now().timestamp()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.end_time = datetime.now().timestamp()
    
    @property
    def elapsed_time(self) -> float:
        """Get the elapsed time in seconds."""
        if self.start_time is None:
            return 0.0
        
        end_time = self.end_time or datetime.now().timestamp()
        return end_time - self.start_time


class ConfigManager:
    """
    A simple configuration manager for applications.
    
    Usage:
        config = ConfigManager("config.json")
        config.set("database.host", "localhost")
        config.set("database.port", 5432)
        config.save()
        
        # Later
        host = config.get("database.host")
        port = config.get("database.port", default=3306)
    """
    
    def __init__(self, config_file: Union[str, Path]) -> None:
        self.config_file = Path(config_file)
        self._config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                self._config = load_json_config(self.config_file)
            except (json.JSONDecodeError, FileNotFoundError):
                self._config = {}
    
    def save(self) -> None:
        """Save configuration to file."""
        save_json_config(self._config, self.config_file)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (supports dot notation like "database.host")
            default: Default value if key is not found
        
        Returns:
            Any: Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key (supports dot notation like "database.host")
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def delete(self, key: str) -> None:
        """
        Delete a configuration value using dot notation.
        
        Args:
            key: Configuration key to delete
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                return
            config = config[k]
        
        if keys[-1] in config:
            del config[keys[-1]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Get the configuration as a dictionary."""
        return self._config.copy()