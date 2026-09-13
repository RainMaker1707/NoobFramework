from json import loads
from pathlib import Path

from .singleton import Singleton

class Config(Singleton):

    def __init__(self, config_path: Path):
        with open(config_path, "r") as file:
            self.config = loads(file.read())

    @property
    def title(self):
        return self.config.get('title')

    @title.setter
    def title(self, value: str):
        self.config['title'] = value

    @property
    def version(self):
        return self.config.get('version')

    @version.setter
    def version(self, value: str):
        raise AttributeError("Config 'version' is read-only to avoid mistakes during code updates")

    @property
    def description(self):
        return self.config.get('description')
    
    @description.setter
    def description(self, value: str):
        raise AttributeError("Config 'description' is read-only to avoid mistakes during code updates")

    @property
    def window(self):
        return self.config.get('window')

    @property
    def panels(self):
        return self.config.get('window').get('panels')
    
    @panels.setter
    def panels(self, value: list):
        self.config.get('window')['panels'] = value
        
