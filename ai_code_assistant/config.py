import os
from pathlib import Path
from typing import Dict, Any
import yaml


class Config:
    def __init__(self, config_file: str = None):
        self.config_file = config_file or self._find_config_file()
        self.config = self._load_config()
    
    def _find_config_file(self) -> str:
        """Find configuration file in current directory or home."""
        current_dir = Path.cwd()
        home_dir = Path.home()
        
        locations = [
            current_dir / ".ai-assist.yaml",
            current_dir / "ai-assist.yaml",
            home_dir / ".ai-assist.yaml",
            home_dir / ".config" / "ai-assist" / "config.yaml"
        ]
        
        for location in locations:
            if location.exists():
                return str(location)
        
        return str(home_dir / ".ai-assist.yaml")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults."""
        defaults = {
            "openai_model": "gpt-4",
            "max_tokens": 1000,
            "temperature": 0.3,
            "exclude_patterns": ["*.log", "*.tmp", "node_modules/*", ".git/*"]
        }
        
        if not os.path.exists(self.config_file):
            self._save_config(defaults)
            return defaults
        
        try:
            with open(self.config_file, "r") as f:
                user_config = yaml.safe_load(f) or {}
            return {**defaults, **user_config}
        except Exception:
            return defaults
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
        self._save_config(self.config)
    
    @property
    def openai_api_key(self) -> str:
        """Get OpenAI API key from environment or config."""
        return os.getenv("OPENAI_API_KEY", self.get("openai_api_key"))