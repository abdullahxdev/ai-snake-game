"""
Configuration constants for the Snake Game
All game parameters can be modified here
"""

# Grid settings
GRID_ROWS = 20
GRID_COLS = 20
CELL_SIZE = 30  # Pixels per cell

# Game settings
DEFAULT_FPS = 10
MIN_FPS = 5
MAX_FPS = 30

# Colors - Dark Theme
DARK_THEME = {
    'background': (18, 18, 18),
    'grid': (40, 40, 40),
    'snake_head': (76, 175, 80),
    'snake_body': (129, 199, 132),
    'food': (244, 67, 54),
    'text': (255, 255, 255),
    'visited': (33, 33, 33),
    'frontier': (66, 66, 66),
    'path': (255, 235, 59),
}

# Colors - Light Theme
LIGHT_THEME = {
    'background': (240, 240, 240),
    'grid': (200, 200, 200),
    'snake_head': (56, 142, 60),
    'snake_body': (139, 195, 74),
    'food': (211, 47, 47),
    'text': (0, 0, 0),
    'visited': (230, 230, 230),
    'frontier': (210, 210, 210),
    'path': (255, 193, 7),
}

# Initial snake position (center of grid)
INITIAL_SNAKE = [(GRID_ROWS // 2, GRID_COLS // 2)]

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = {
    'UP': UP,
    'DOWN': DOWN,
    'LEFT': LEFT,
    'RIGHT': RIGHT
}

# AI settings
AI_HEURISTIC = 'manhattan'  # 'manhattan' or 'euclidean'
AI_ALGORITHM = 'astar'       # 'bfs' or 'astar'
SHOW_SEARCH_VISUALIZATION = True
DYNAMIC_REPLANNING = True

# Logging
ENABLE_LOGGING = True
LOG_DIR = 'logs'