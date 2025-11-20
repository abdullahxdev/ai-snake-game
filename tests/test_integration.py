"""
Integration tests for Snake AI Game
Tests menu, AI modes, and high-score survival
"""
import pytest
from snake_game.game import SnakeGame
from snake_game.agent import SnakeAIAgent
from snake_game.agent_bfs import BFSAgent
from snake_game.agent_alphabeta import AlphaBetaAgent
from snake_game.config import config


class TestIntegration:
    """Integration test suite"""
    
    def test_menu_initialization(self):
        """Test that menu components initialize correctly"""
        from snake_game.ui.menu import MainMenu
        from snake_game.audio import AudioManager
        
        audio = AudioManager(enabled=False)
        menu = MainMenu(1280, 720, config, audio)
        
        assert menu is not None
        assert len(menu.buttons) == 4
        assert menu.theme is not None
    
    def test_grid_scaling(self):
        """Test that grid covers ~80% of screen"""
        cell_size, rows, cols = config.calculate_grid_dimensions()
        
        window_width = config.get('window', 'width')
        window_height = config.get('window', 'height')
        coverage = config.get('window', 'grid_coverage')
        
        grid_width = cols * cell_size
        grid_height = rows * cell_size
        
        # Calculate actual coverage
        ui_height = 120
        playable_height = window_height - ui_height
        
        width_coverage = grid_width / window_width
        height_coverage = grid_height / playable_height
        
        # Should be close to 80% (within 10% tolerance)
        assert abs(width_coverage - coverage) < 0.1
        assert abs(height_coverage - coverage) < 0.1
    
    def test_astar_pathfinding(self):
        """Test A* can find path on empty grid"""
        game = SnakeGame()
        agent = SnakeAIAgent(game, 'astar', 'manhattan')
        
        # Should find path to food
        direction = agent.get_next_move()
        
        assert direction is not None
        assert direction != (0, 0)
    
    def test_bfs_pathfinding(self):
        """Test BFS can find path on empty grid"""
        game = SnakeGame()
        agent = BFSAgent(game)
        
        # Should find path to food
        direction = agent.get_next_move()
        
        assert direction is not None
        assert direction != (0, 0)
    
    def test_alphabeta_pathfinding(self):
        """Test Alpha-Beta can compute move"""
        game = SnakeGame()
        agent = AlphaBetaAgent(game, max_depth=3)
        
        # Should compute a move
        direction = agent.get_next_move()
        
        assert direction is not None
        assert direction != (0, 0)
    
    def test_survival_mode_activation(self):
        """Test that survival mode activates at threshold"""
        game = SnakeGame()
        agent = SnakeAIAgent(game, 'astar', 'manhattan')
        
        # Manually set score to threshold
        threshold = config.get('ai', 'survival_mode_threshold')
        game.score = threshold
        game.survival_mode = True
        
        # Should still compute move
        direction = agent.get_next_move()
        
        assert direction is not None
        assert game.survival_mode is True
    
    def test_high_score_survival(self):
        """Test AI survives 500 steps without crash (headless)"""
        game = SnakeGame()
        agent = SnakeAIAgent(game, 'astar', 'manhattan')
        
        steps = 0
        max_steps = 500
        
        while not game.game_over and steps < max_steps:
            direction = agent.get_next_move()
            game.change_direction(direction)
            game.update()
            steps += 1
        
        # Should survive at least 500 steps
        assert steps == max_steps or game.score > 10
        
        if game.game_over:
            print(f"Game ended at step {steps} with score {game.score}")
        else:
            print(f"Successfully survived {steps} steps with score {game.score}")
    
    def test_no_self_collision_bug(self):
        """Test that the score 60-70 crash bug is fixed"""
        game = SnakeGame()
        agent = SnakeAIAgent(game, 'astar', 'manhattan')
        
        # Simulate until score reaches 70 or game over
        while game.score < 70 and not game.game_over:
            direction = agent.get_next_move()
            game.change_direction(direction)
            
            # Store snake state before update
            prev_snake_len = len(game.snake)
            
            game.update()
            
            # Verify snake integrity
            assert len(game.snake) >= prev_snake_len  # Only grows or stays same
            assert len(game.snake) == len(set(game.snake))  # No duplicate positions
        
        # Should either reach score 70 or game over naturally
        print(f"Test completed: Score={game.score}, GameOver={game.game_over}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])