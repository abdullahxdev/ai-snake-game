"""
Configuration manager for Snake AI Game
Loads and saves settings from config.yaml
"""
import yaml
import os
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    'window': {
        'width': 1280,
        'height': 720,
        'title': 'Snake AI Game',
        'grid_coverage': 0.8
    },
    'grid': {
        'cell_size': 30,
        'rows': 20,
        'cols': 20
    },
    'game': {
        'default_fps': 12,
        'min_fps': 5,
        'max_fps': 30,
        'initial_snake_length': 3
    },
    'ai': {
        'default_mode': 'astar',
        'heuristic': 'manhattan',
        'show_visualization': True,
        'dynamic_replanning': True,
        'alphabeta_depth': 4,
        'survival_mode_threshold': 50
    },
    'audio': {
        'enabled': True,
        'volume': 70,
        'sound_effects': True,
        'background_music': False
    },
    'visual': {
        'default_theme': 'neon',
        'show_grid': True,
        'show_eyes': True,
        'animate_background': True,
        'show_path_overlay': True,
        'gradient_body': True
    },
    'menu': {
        'animation_speed': 1.0,
        'ghost_snakes': 5,
        'parallax_layers': 3
    },
    'performance': {
        'headless_mode': False,
        'vsync': True,
        'benchmark_mode': False
    },
    'logging': {
        'enabled': True,
        'log_dir': 'logs',
        'level': 'INFO'
    }
}


class ConfigManager:
    """Manages game configuration"""
    
    def __init__(self, config_path='config.yaml'):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to config file
        """
        self.config_path = config_path
        self.config = DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = yaml.safe_load(f)
                    if loaded_config:
                        self._deep_update(self.config, loaded_config)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
                print("Using default configuration")
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")
    
    def _deep_update(self, base, update):
        """Recursively update nested dictionary"""
        for key, value in update.items():
            if isinstance(value, dict) and key in base:
                self._deep_update(base[key], value)
            else:
                base[key] = value
    
    def get(self, *keys):
        """
        Get configuration value by path
        
        Args:
            *keys: Path to configuration value
            
        Returns:
            Configuration value
        """
        value = self.config
        for key in keys:
            value = value[key]
        return value
    
    def set(self, *keys, value):
        """
        Set configuration value by path
        
        Args:
            *keys: Path to configuration value
            value: Value to set
        """
        config = self.config
        for key in keys[:-1]:
            config = config[key]
        config[keys[-1]] = value
    
    def calculate_grid_dimensions(self):
        """
        Calculate optimal grid dimensions based on window size and coverage
        
        Returns:
            Tuple of (cell_size, rows, cols)
        """
        window_width = self.get('window', 'width')
        window_height = self.get('window', 'height')
        coverage = self.get('window', 'grid_coverage')
        
        # Reserve space for UI (bottom bar)
        ui_height = 120
        playable_height = window_height - ui_height
        
        # Calculate available space for grid
        available_width = int(window_width * coverage)
        available_height = int(playable_height * coverage)
        
        # Start with desired cell size
        desired_cell_size = 30
        
        # Calculate how many cells fit
        cols = available_width // desired_cell_size
        rows = available_height // desired_cell_size
        
        # Ensure minimum grid size
        cols = max(cols, 15)
        rows = max(rows, 15)
        
        # Recalculate cell size to fit exactly
        cell_size_width = available_width // cols
        cell_size_height = available_height // rows
        cell_size = min(cell_size_width, cell_size_height)
        
        # Update config
        self.set('grid', 'cell_size', value=cell_size)
        self.set('grid', 'rows', value=rows)
        self.set('grid', 'cols', value=cols)
        
        return cell_size, rows, cols


# Global config instance
config = ConfigManager()