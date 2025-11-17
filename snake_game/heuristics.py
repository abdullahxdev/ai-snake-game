"""
Heuristic functions for A* search algorithm
"""
from snake_game.utils import manhattan_distance, euclidean_distance


def manhattan_heuristic(pos, goal):
    """
    Manhattan distance heuristic (admissible for grid-based movement)
    
    Args:
        pos: Current position (x, y)
        goal: Goal position (x, y)
        
    Returns:
        Heuristic value
    """
    return manhattan_distance(pos, goal)


def euclidean_heuristic(pos, goal):
    """
    Euclidean distance heuristic (admissible but less informed for grid)
    
    Args:
        pos: Current position (x, y)
        goal: Goal position (x, y)
        
    Returns:
        Heuristic value
    """
    return euclidean_distance(pos, goal)


def get_heuristic(name):
    """
    Get heuristic function by name
    
    Args:
        name: 'manhattan' or 'euclidean'
        
    Returns:
        Heuristic function
    """
    heuristics = {
        'manhattan': manhattan_heuristic,
        'euclidean': euclidean_heuristic
    }
    
    return heuristics.get(name.lower(), manhattan_heuristic)