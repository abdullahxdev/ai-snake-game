"""
Utility functions for the Snake Game
"""
import os
import logging
from datetime import datetime


def setup_logging(run_id=None):
    """
    Set up logging for AI runs
    
    Args:
        run_id: Optional identifier for this run
        
    Returns:
        Logger instance
    """
    # Import here to avoid circular dependency
    from snake_game.config import config
    
    if not config.get('logging', 'enabled'):
        return None
    
    # Create logs directory if it doesn't exist
    log_dir = config.get('logging', 'log_dir')
    os.makedirs(log_dir, exist_ok=True)
    
    # Create unique log file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'ai_run_{timestamp}.log')
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.get('logging', 'level')),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting new AI run: {run_id or 'unnamed'}")
    
    return logger


def manhattan_distance(pos1, pos2):
    """
    Calculate Manhattan distance between two positions
    
    Args:
        pos1: Tuple (x, y)
        pos2: Tuple (x, y)
        
    Returns:
        Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def euclidean_distance(pos1, pos2):
    """
    Calculate Euclidean distance between two positions
    
    Args:
        pos1: Tuple (x, y)
        pos2: Tuple (x, y)
        
    Returns:
        Euclidean distance
    """
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def is_valid_position(pos, grid_rows, grid_cols):
    """
    Check if position is within grid bounds
    
    Args:
        pos: Tuple (x, y)
        grid_rows: Number of rows
        grid_cols: Number of columns
        
    Returns:
        True if valid, False otherwise
    """
    x, y = pos
    return 0 <= x < grid_cols and 0 <= y < grid_rows


def get_neighbors(pos, grid_rows, grid_cols):
    """
    Get valid neighboring positions (up, down, left, right)
    
    Args:
        pos: Tuple (x, y)
        grid_rows: Number of rows
        grid_cols: Number of columns
        
    Returns:
        List of valid neighbor positions
    """
    x, y = pos
    neighbors = []
    
    # Four directions: up, down, left, right
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    for dx, dy in directions:
        new_pos = (x + dx, y + dy)
        if is_valid_position(new_pos, grid_rows, grid_cols):
            neighbors.append(new_pos)
    
    return neighbors


def direction_to_next_pos(current_pos, next_pos):
    """
    Calculate direction from current position to next position
    
    Args:
        current_pos: Tuple (x, y)
        next_pos: Tuple (x, y)
        
    Returns:
        Direction tuple (dx, dy)
    """
    dx = next_pos[0] - current_pos[0]
    dy = next_pos[1] - current_pos[1]
    return (dx, dy)