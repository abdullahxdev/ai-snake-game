"""
BFS (Breadth-First Search) AI agent for Snake
Uses unweighted shortest path search
"""
import logging
from collections import deque


def get_neighbors(pos, grid_rows, grid_cols):
    """Get valid neighboring positions"""
    x, y = pos
    neighbors = []
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    for dx, dy in directions:
        new_pos = (x + dx, y + dy)
        if 0 <= new_pos[0] < grid_cols and 0 <= new_pos[1] < grid_rows:
            neighbors.append(new_pos)
    
    return neighbors


class BFSAgent:
    """AI agent using Breadth-First Search"""
    
    def __init__(self, game):
        """
        Initialize BFS agent
        
        Args:
            game: SnakeGame instance
        """
        self.game = game
        self.current_path = []
        self.logger = logging.getLogger(__name__)
    
    def get_next_move(self):
        """
        Decide the next move using BFS
        
        Returns:
            Direction tuple (dx, dy)
        """
        # Always replan for dynamic environment
        self._plan_path()
        
        # Follow path if available
        if self.current_path and len(self.current_path) > 1:
            next_pos = self.current_path[1]
            head = self.game.snake[0]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            self.current_path.pop(0)
            return direction
        
        # Fallback: tail chase
        return self._tail_chase_fallback()
    
    def _plan_path(self):
        """Plan path using BFS"""
        head = self.game.snake[0]
        food = self.game.food
        obstacles = set(self.game.snake[1:])
        
        # BFS search
        queue = deque([(head, [head])])
        visited = {head}
        
        while queue:
            current, path = queue.popleft()
            
            if current == food:
                self.current_path = path
                self.logger.info(f"BFS found path: length={len(path)}")
                return
            
            for neighbor in get_neighbors(current, self.game.grid_rows, self.game.grid_cols):
                if neighbor not in visited and neighbor not in obstacles:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        # No path found
        self.current_path = []
        self.logger.warning("BFS: No path to food")
    
    def _tail_chase_fallback(self):
        """Chase own tail as fallback"""
        head = self.game.snake[0]
        tail = self.game.snake[-1]
        obstacles = set(self.game.snake[1:-1])
        
        # BFS to tail
        queue = deque([(head, [head])])
        visited = {head}
        
        while queue:
            current, path = queue.popleft()
            
            if current == tail:
                if len(path) > 1:
                    next_pos = path[1]
                    direction = (next_pos[0] - head[0], next_pos[1] - head[1])
                    return direction
                break
            
            for neighbor in get_neighbors(current, self.game.grid_rows, self.game.grid_cols):
                if neighbor not in visited and neighbor not in obstacles:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        # Last resort: any safe move
        return self._find_safe_move()
    
    def _find_safe_move(self):
        """Find any safe move"""
        head = self.game.snake[0]
        for neighbor in get_neighbors(head, self.game.grid_rows, self.game.grid_cols):
            if self.game.is_position_safe(neighbor):
                direction = (neighbor[0] - head[0], neighbor[1] - head[1])
                return direction
        return self.game.direction
    
    def get_visualization_data(self):
        """Get visualization data for rendering"""
        return {
            'visited': set(),
            'frontier': set(),
            'path': self.current_path
        }