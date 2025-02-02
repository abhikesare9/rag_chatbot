
import json
import os
from RagLogger import SingletonLogger
class MLConfigParser:
    _instance = None


    def __init__(self):
        self.logger = SingletonLogger().get_logger()
    def __new__(cls, config_file='config.json'):
        if cls._instance is None:
            cls._instance = super(MLConfigParser, cls).__new__(cls)
            cls._instance.config_file = config_file
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as file:
                    cls._instance.config = json.load(file)
            else:
                cls._instance.config = {}
                cls._instance.save()  # Create a new file if it doesn't exist
        
        return cls._instance

    def get(self, section, option):
        try:
            """Get a value from the configuration."""
            return self.config.get(section, {}).get(option)
        except Exception as e:
            self.logger.error("Failed to get value for {e}")
            raise e

    def set(self, section, option, value):
        try:
            """Set a value in the configuration."""
            if section not in self.config:
                self.config[section] = {}
            self.config[section][option] = value
            self.save()
        except Exception as e:
            self.logger.error("Failed to set value for {e}")
            raise e

    def save(self):
        try:
            """Save the configuration back to the file."""
            with open(self.config_file, 'w') as file:
                json.dump(self.config, file, indent=4)
        except Exception as e:
            self.logger.error("Failed to save the value {e}")
            raise e

    

