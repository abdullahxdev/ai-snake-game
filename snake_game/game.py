"""
Snake Game Engine
Handles game logic, snake movement, collision detection, and scoring
"""
import random
from snake_game.config import (
    GRID_ROWS, GRID_COLS, INITIAL_SNAKE, UP, DOWN, LEFT, RIGHT
)


class SnakeGame:
    """Main game engine for Snake"""
    
    def __init__(self, grid_rows=GRID_ROWS, grid_cols=GRID_COLS):
        """
        Initialize the Snake game
        
        Args:
            grid_rows: Number of rows in the grid
            grid_cols: Number of columns in the grid
        """
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.reset()
    
    def reset(self):
        """Reset the game to initial state"""
        # Snake starts in the center
        self.snake = list(INITIAL_SNAKE)
        self.direction = RIGHT
        self.food = self._spawn_food()
        self.score = 0
        self.game_over = False
        self.moves = 0
        
    def _spawn_food(self):
        """
        Spawn food at a random empty position
        
        Returns:
            Food position (x, y)
        """
        while True:
            food = (
                random.randint(0, self.grid_cols - 1),
                random.randint(0, self.grid_rows - 1)
            )
            if food not in self.snake:
                return food
    
    def change_direction(self, new_direction):
        """
        Change snake direction (prevents 180-degree turns)
        
        Args:
            new_direction: New direction tuple (dx, dy)
        """
        # Prevent reversing into itself
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction
    
    def update(self):
        """
        Update game state for one tick
        
        Returns:
            True if game continues, False if game over
        """
        if self.game_over:
            return False
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if not (0 <= new_head[0] < self.grid_cols and 
                0 <= new_head[1] < self.grid_rows):
            self.game_over = True
            return False
        
        # Check self-collision
        if new_head in self.snake:
            self.game_over = True
            return False
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 1
            self.food = self._spawn_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
        
        self.moves += 1
        return True
    
    def get_state(self):
        """
        Get current game state
        
        Returns:
            Dictionary containing game state
        """
        return {
            'snake': list(self.snake),
            'food': self.food,
            'score': self.score,
            'game_over': self.game_over,
            'moves': self.moves,
            'direction': self.direction
        }
    
    def is_position_safe(self, pos):
        """
        Check if position is safe (not wall or snake body)
        
        Args:
            pos: Position to check (x, y)
            
        Returns:
            True if safe, False otherwise
        """
        x, y = pos
        
        # Check bounds
        if not (0 <= x < self.grid_cols and 0 <= y < self.grid_rows):
            return False
        
        # Check snake body (excluding head for movement check)
        if pos in self.snake[1:]:
            return False
        
        return True
    
    def get_available_spaces(self):
        """
        Get count of available empty spaces
        
        Returns:
            Number of empty cells
        """
        total_cells = self.grid_rows * self.grid_cols
        occupied = len(self.snake)
        return total_cells - occupied