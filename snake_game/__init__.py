"""
Snake AI Game Package
A complete Snake game with AI agents using BFS and A* search algorithms
"""

__version__ = '1.0.0'
__author__ = 'Snake AI Project'

from snake_game.game import SnakeGame
from snake_game.agent import SnakeAIAgent
from snake_game.renderer import GameRenderer

__all__ = ['SnakeGame', 'SnakeAIAgent', 'GameRenderer']