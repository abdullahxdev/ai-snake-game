"""
Unit tests for search algorithms
Tests BFS and A* implementations
"""
import pytest
from snake_game.search import bfs_search, astar_search, simulate_snake_movement
from snake_game.config import GRID_ROWS, GRID_COLS


class TestSearchAlgorithms:
    """Test suite for search algorithms"""
    
    def test_bfs_finds_path(self):
        """Test that BFS finds a path when one exists"""
        start = (0, 0)
        goal = (5, 5)
        obstacles = set()
        
        result = bfs_search(start, goal, obstacles, GRID_ROWS, GRID_COLS)
        
        assert result.found is True
        assert result.path[0] == start
        assert result.path[-1] == goal
        assert len(result.path) > 0
    
    def test_bfs_no_path(self):
        """Test that BFS returns no path when blocked"""
        start = (0, 0)
        goal = (5, 5)
        
        # Create wall blocking the goal
        obstacles = set()
        for x in range(GRID_COLS):
            obstacles.add((x, 4))
        
        result = bfs_search(start, goal, obstacles, GRID_ROWS, GRID_COLS)
        
        assert result.found is False
        assert len(result.path) == 0
    
    def test_astar_finds_path(self):
        """Test that A* finds a path when one exists"""
        start = (0, 0)
        goal = (5, 5)
        obstacles = set()
        
        result = astar_search(start, goal, obstacles, GRID_ROWS, GRID_COLS, 'manhattan')
        
        assert result.found is True
        assert result.path[0] == start
        assert result.path[-1] == goal
        assert len(result.path) > 0
    
    def test_astar_optimal_path(self):
        """Test that A* finds optimal path length"""
        start = (0, 0)
        goal = (5, 5)
        obstacles = set()
        
        result = astar_search(start, goal, obstacles, GRID_ROWS, GRID_COLS, 'manhattan')
        
        # Manhattan distance is 10, so path should be around that length
        expected_min_length = 10 + 1  # +1 because path includes start
        assert len(result.path) == expected_min_length
    
    def test_astar_vs_bfs(self):
        """Test that A* expands fewer nodes than BFS"""
        start = (0, 0)
        goal = (10, 10)
        obstacles = set()
        
        bfs_result = bfs_search(start, goal, obstacles, GRID_ROWS, GRID_COLS)
        astar_result = astar_search(start, goal, obstacles, GRID_ROWS, GRID_COLS, 'manhattan')
        
        # A* should expand fewer nodes due to heuristic guidance
        assert astar_result.nodes_expanded < bfs_result.nodes_expanded
    
    def test_simulate_snake_movement_safe(self):
        """Test simulation of safe snake movement"""
        snake = [(5, 5), (5, 4), (5, 3)]
        path = [(5, 5), (6, 5), (7, 5)]
        
        result = simulate_snake_movement(snake, path)
        
        assert result is True
    
    def test_simulate_snake_movement_collision(self):
        """Test simulation detects self-collision"""
        snake = [(5, 5), (6, 5), (7, 5), (7, 4), (6, 4), (5, 4)]
        path = [(5, 5), (5, 4)]  # Would hit body
        
        result = simulate_snake_movement(snake, path)
        
        assert result is False
    
    def test_heuristic_admissible(self):
        """Test that Manhattan heuristic is admissible"""
        start = (0, 0)
        goal = (10, 10)
        obstacles = set()
        
        result = astar_search(start, goal, obstacles, GRID_ROWS, GRID_COLS, 'manhattan')
        
        # Path cost should equal Manhattan distance for optimal path
        manhattan_dist = abs(goal[0] - start[0]) + abs(goal[1] - start[1])
        assert result.path_cost == manhattan_dist


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_start_equals_goal(self):
        """Test when start position equals goal position"""
        pos = (5, 5)
        obstacles = set()
        
        result = astar_search(pos, pos, obstacles, GRID_ROWS, GRID_COLS)
        
        assert result.found is True
        assert len(result.path) == 1
    
    def test_adjacent_positions(self):
        """Test pathfinding between adjacent positions"""
        start = (5, 5)
        goal = (5, 6)
        obstacles = set()
        
        result = astar_search(start, goal, obstacles, GRID_ROWS, GRID_COLS)
        
        assert result.found is True
        assert len(result.path) == 2
    
    def test_goal_is_obstacle(self):
        """Test when goal is blocked by obstacle"""
        start = (0, 0)
        goal = (5, 5)
        obstacles = {goal}
        
        result = astar_search(start, goal, obstacles, GRID_ROWS, GRID_COLS)
        
        assert result.found is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])