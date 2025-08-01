"""
Tests for shared utilities module.

This module contains unit tests for the shared utilities to ensure
they work correctly across different applications.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from shared.utils import (
    get_project_root,
    load_json_config,
    save_json_config,
    get_file_hash,
    ensure_directory,
    Timer,
    ConfigManager
)


class TestUtils:
    """Test cases for utility functions."""
    
    def test_get_project_root(self):
        """Test that get_project_root returns the correct path."""
        root = get_project_root()
        assert root.is_dir()
        assert (root / "pyproject.toml").exists()
        assert (root / "shared").exists()
    
    def test_load_save_json_config(self):
        """Test JSON configuration loading and saving."""
        test_config = {
            "app": {
                "name": "test-app",
                "version": "1.0.0"
            },
            "database": {
                "host": "localhost",
                "port": 5432
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = Path(f.name)
        
        try:
            # Test saving
            save_json_config(test_config, config_path)
            assert config_path.exists()
            
            # Test loading
            loaded_config = load_json_config(config_path)
            assert loaded_config == test_config
            
        finally:
            config_path.unlink()
    
    def test_load_json_config_file_not_found(self):
        """Test that load_json_config raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            load_json_config("nonexistent_file.json")
    
    def test_get_file_hash(self):
        """Test file hash calculation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Hello, World!")
            temp_path = Path(f.name)
        
        try:
            # Test SHA256 hash
            hash_sha256 = get_file_hash(temp_path, "sha256")
            assert len(hash_sha256) == 64  # SHA256 produces 64-char hex string
            assert hash_sha256 == "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
            
            # Test MD5 hash
            hash_md5 = get_file_hash(temp_path, "md5")
            assert len(hash_md5) == 32  # MD5 produces 32-char hex string
            
        finally:
            temp_path.unlink()
    
    def test_get_file_hash_file_not_found(self):
        """Test that get_file_hash raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            get_file_hash("nonexistent_file.txt")
    
    def test_get_file_hash_invalid_algorithm(self):
        """Test that get_file_hash raises ValueError for invalid algorithms."""
        with tempfile.NamedTemporaryFile() as f:
            with pytest.raises(ValueError):
                get_file_hash(f.name, "invalid_algorithm")
    
    def test_ensure_directory(self):
        """Test directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = Path(temp_dir) / "nested" / "directory" / "structure"
            
            # Directory shouldn't exist initially
            assert not test_dir.exists()
            
            # Create directory
            result = ensure_directory(test_dir)
            
            # Check that directory was created and returned
            assert test_dir.exists()
            assert test_dir.is_dir()
            assert result == test_dir


class TestTimer:
    """Test cases for Timer context manager."""
    
    def test_timer_basic_functionality(self):
        """Test basic timer functionality."""
        with Timer() as timer:
            pass
        
        assert timer.elapsed_time >= 0
        assert timer.start_time is not None
        assert timer.end_time is not None
    
    def test_timer_elapsed_time_increases(self):
        """Test that elapsed time increases during execution."""
        import time
        
        with Timer() as timer:
            time.sleep(0.01)  # Sleep for 10ms
        
        assert timer.elapsed_time >= 0.01


class TestConfigManager:
    """Test cases for ConfigManager class."""
    
    def test_config_manager_basic_operations(self):
        """Test basic configuration operations."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            config_path = Path(f.name)
        
        try:
            config = ConfigManager(config_path)
            
            # Test setting values
            config.set("app.name", "test-app")
            config.set("app.version", "1.0.0")
            config.set("database.host", "localhost")
            config.set("database.port", 5432)
            
            # Test getting values
            assert config.get("app.name") == "test-app"
            assert config.get("app.version") == "1.0.0"
            assert config.get("database.host") == "localhost"
            assert config.get("database.port") == 5432
            
            # Test default values
            assert config.get("nonexistent.key", "default") == "default"
            
            # Test saving and loading
            config.save()
            
            # Create new instance and verify data persists
            config2 = ConfigManager(config_path)
            assert config2.get("app.name") == "test-app"
            assert config2.get("database.port") == 5432
            
        finally:
            config_path.unlink()
    
    def test_config_manager_nested_keys(self):
        """Test nested key operations."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            config_path = Path(f.name)
        
        try:
            config = ConfigManager(config_path)
            
            # Set deeply nested values
            config.set("level1.level2.level3.value", "deep_value")
            assert config.get("level1.level2.level3.value") == "deep_value"
            
            # Test intermediate level access
            level2 = config.get("level1.level2")
            assert isinstance(level2, dict)
            assert level2["level3"]["value"] == "deep_value"
            
        finally:
            config_path.unlink()
    
    def test_config_manager_delete(self):
        """Test configuration key deletion."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            config_path = Path(f.name)
        
        try:
            config = ConfigManager(config_path)
            
            # Set and then delete a value
            config.set("test.key", "value")
            assert config.get("test.key") == "value"
            
            config.delete("test.key")
            assert config.get("test.key") is None
            
        finally:
            config_path.unlink()
    
    def test_config_manager_to_dict(self):
        """Test configuration dictionary export."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            config_path = Path(f.name)
        
        try:
            config = ConfigManager(config_path)
            config.set("app.name", "test")
            config.set("app.version", "1.0")
            
            config_dict = config.to_dict()
            expected = {
                "app": {
                    "name": "test",
                    "version": "1.0"
                }
            }
            
            assert config_dict == expected
            
        finally:
            config_path.unlink()


if __name__ == "__main__":
    pytest.main([__file__])