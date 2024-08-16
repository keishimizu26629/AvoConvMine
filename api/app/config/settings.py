import os
from typing import List

class Settings:
    def __init__(self):
        self.ATTRIBUTE_PREFIXES_TO_REMOVE: List[str] = [
            "personal information ",
            "personal info ",
            "hobbies ",
            "interests ",
            "professional info ",
            "professional information "
        ]
        self._load_env()

    def _load_env(self):
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value

    def __getattr__(self, name):
        return os.getenv(name, getattr(self, name, None))
