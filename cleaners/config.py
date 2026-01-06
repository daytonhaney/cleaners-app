#!/usr/bin/env python3
"""Configuration management for CleanersApp"""

import os
import json
from pathlib import Path

CONFIG_FILE = "cleaners_config.json"

# Default configuration
DEFAULT_CONFIG = {
    "database": {
        "path": "./business_data.db",
        "backup_enabled": True,
        "backup_interval_days": 7,
        "backup_location": "./backups/",
    },
    "business": {
        "name": "CleanersApp Service",
        "phone": "",
        "email": "",
        "address": "",
        "tax_rate": 0.08,
        "senior_discount": 0.15,
        "senior_age": 65,
    },
    "ui": {
        "theme": "default",  # default, dark, light
        "show_animations": True,
        "auto_save": True,
        "receipt_enabled": True,
    },
    "validation": {
        "max_square_footage": 10000,
        "min_square_footage": 100,
        "max_customer_name_length": 50,
        "min_customer_name_length": 2,
        "max_address_length": 100,
    },
}


def load_config():
    """Load configuration from file or create default"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            # Merge with defaults to ensure all keys exist
            return {**DEFAULT_CONFIG, **config}
        else:
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG


def save_config(config):
    """Save configuration to file"""
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE) or ".", exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False


def get_config(key_path, default=None):
    """Get specific config value using dot notation"""
    config = load_config()
    keys = key_path.split(".")
    value = config

    try:
        for key in keys:
            value = value[key]
        return value if value is not None else default
    except (KeyError, TypeError):
        return default


def set_config(key_path, value):
    """Set specific config value using dot notation"""
    config = load_config()
    keys = key_path.split(".")
    current = config

    # Navigate to the parent of the target key
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]

    # Set the final value
    current[keys[-1]] = value
    return save_config(config)


# Initialize config on import
config = load_config()
