"""
Snake Game Engine - UPDATED
Handles game logic with improved collision detection and survival mode
CHANGELOG: Fixed score 60-70 crash by improving body update logic and adding survival mode
"""
import random
from snake_game.config import config


class SnakeGame:
    """Main game engine for Snake - BUGFIXED VERSION"""
    
    def __init__(self):
        """Initialize the Snake game with dynamic grid sizing"""
        # Calculate grid dimensions dynamically
        cell_size, rows, cols = config.calculate_grid_dimensions()
        
        self.grid_rows = rows
        self.grid_cols = cols
        self.cell_size = cell_size
        
        # Initialize game state variables first
        self.snake = []
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = (0, 0)  # Temporary
        self.score = 0
        self.game_over = False
        self.moves = 0
        self.survival_mode = False
        
        # Now properly reset the game
        self.reset()
    
    def reset(self):
        """Reset the game to initial state"""
        # Snake starts in the center with initial length
        initial_length = config.get('game', 'initial_snake_length')
        center_x = self.grid_cols // 2
        center_y = self.grid_rows // 2
        
        self.snake = [(center_x, center_y)]
        
        # Grow initial snake to the left
        for i in range(1, initial_length):
            self.snake.append((center_x - i, center_y))
        
        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)  # Queued direction
        self.food = self._spawn_food()
        self.score = 0
        self.game_over = False
        self.moves = 0
        self.survival_mode = False
    
    def _spawn_food(self):
        """
        Spawn food at a random empty position
        BUGFIX: Ensures food never spawns on snake body
        """
        # Quick check if grid is too full
        if len(self.snake) >= self.grid_rows * self.grid_cols - 1:
            # Grid is full or nearly full
            return self.snake[0]  # Just return head position (game should be over)
        
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            food = (
                random.randint(0, self.grid_cols - 1),
                random.randint(0, self.grid_rows - 1)
            )
            if food not in self.snake:
                return food
            attempts += 1
        
        # Fallback: find any empty cell systematically
        for x in range(self.grid_cols):
            for y in range(self.grid_rows):
                pos = (x, y)
                if pos not in self.snake:
                    return pos
        
        # Grid is completely full (game won!)
        return (0, 0)
    
    def change_direction(self, new_direction):
        """
        Change snake direction (prevents 180-degree turns)
        BUGFIX: Uses queued direction system to prevent input loss
        
        Args:
            new_direction: New direction tuple (dx, dy)
        """
        # Prevent reversing into itself
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite and new_direction != (0, 0):
            self.next_direction = new_direction
    
    def update(self):
        """
        Update game state for one tick
        BUGFIX: Improved body update logic to prevent desync at high scores
        
        Returns:
            True if game continues, False if game over
        """
        if self.game_over:
            return False
        
        # Apply queued direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if not (0 <= new_head[0] < self.grid_cols and 
                0 <= new_head[1] < self.grid_rows):
            self.game_over = True
            return False
        
        # Check self-collision BEFORE adding new head
        # This prevents the off-by-one error that caused crashes at high scores
        if new_head in self.snake:
            self.game_over = True
            return False
        
        # Check food collision
        ate_food = (new_head == self.food)
        
        # Move snake: add new head first
        self.snake.insert(0, new_head)
        
        # Remove tail only if no food eaten
        if ate_food:
            self.score += 1
            self.food = self._spawn_food()
            
            # Enable survival mode at threshold
            survival_threshold = config.get('ai', 'survival_mode_threshold')
            if self.score >= survival_threshold:
                self.survival_mode = True
        else:
            # Remove tail (no growth)
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
            'direction': self.direction,
            'survival_mode': self.survival_mode
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
    
    def get_safe_neighbors(self, pos):
        """
        Get all safe neighboring positions
        
        Args:
            pos: Current position
            
        Returns:
            List of safe neighbor positions
        """
        x, y = pos
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if self.is_position_safe(neighbor):
                neighbors.append(neighbor)
        
        return neighbors