"""
Unit tests for game logic
Tests Snake game mechanics
"""
import pytest
from snake_game.game import SnakeGame
from snake_game.config import RIGHT, LEFT, UP, DOWN


class TestGameLogic:
    """Test suite for game logic"""
    
    def setup_method(self):
        """Setup before each test"""
        self.game = SnakeGame(grid_rows=20, grid_cols=20)
    
    def test_initial_state(self):
        """Test initial game state"""
        assert len(self.game.snake) == 1
        assert self.game.score == 0
        assert self.game.game_over is False
        assert self.game.food is not None
    
    def test_snake_movement(self):
        """Test basic snake movement"""
        initial_head = self.game.snake[0]
        self.game.update()
        new_head = self.game.snake[0]
        
        # Snake should have moved right
        assert new_head[0] == initial_head[0] + 1
        assert new_head[1] == initial_head[1]
    
    def test_snake_growth(self):
        """Test snake grows when eating food"""
        initial_length = len(self.game.snake)
        
        # Place food in front of snake
        head = self.game.snake[0]
        self.game.food = (head[0] + 1, head[1])
        
        self.game.update()
        
        assert len(self.game.snake) == initial_length + 1
        assert self.game.score == 1
    
    def test_wall_collision(self):
        """Test collision with walls"""
        # Move snake to edge
        self.game.snake = [(19, 10)]
        self.game.direction = RIGHT
        
        self.game.update()
        
        assert self.game.game_over is True
    
    def test_self_collision(self):
        """Test collision with self"""
        # Create snake that will collide with itself
        self.game.snake = [(5, 5), (5, 4), (5, 3), (6, 3), (6, 4), (6, 5)]
        self.game.direction = DOWN
        
        self.game.update()
        
        assert self.game.game_over is True
    
    def test_direction_change(self):
        """Test valid direction changes"""
        self.game.direction = RIGHT
        self.game.change_direction(UP)
        
        assert self.game.direction == UP
    
    def test_prevent_reverse(self):
        """Test prevention of 180-degree turns"""
        self.game.snake = [(5, 5), (4, 5)]  # Snake going right
        self.game.direction = RIGHT
        self.game.change_direction(LEFT)  # Try to reverse
        
        assert self.game.direction == RIGHT  # Should not change
    
    def test_food_spawn_not_on_snake(self):
        """Test that food doesn't spawn on snake"""
        # Fill most of the grid with snake
        self.game.snake = [(x, y) for x in range(20) for y in range(19)]
        food = self.game._spawn_food()
        
        assert food not in self.game.snake
    
    def test_reset(self):
        """Test game reset"""
        # Play some moves
        self.game.update()
        self.game.update()
        self.game.score = 5
        
        self.game.reset()
        
        assert len(self.game.snake) == 1
        assert self.game.score == 0
        assert self.game.game_over is False
        assert self.game.moves == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])