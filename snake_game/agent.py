"""
AI Agent for playing Snake using search algorithms
Includes tail-chasing fallback and dynamic replanning
"""
import logging
from snake_game.search import astar_search, bfs_search, simulate_snake_movement
from snake_game.config import AI_ALGORITHM, AI_HEURISTIC, DYNAMIC_REPLANNING
from snake_game.utils import get_neighbors


class SnakeAIAgent:
    """AI agent that uses search algorithms to play Snake"""
    
    def __init__(self, game, algorithm='astar', heuristic='manhattan'):
        """
        Initialize AI agent
        
        Args:
            game: SnakeGame instance
            algorithm: 'bfs' or 'astar'
            heuristic: 'manhattan' or 'euclidean' (for A*)
        """
        self.game = game
        self.algorithm = algorithm
        self.heuristic = heuristic
        self.current_path = []
        self.search_result = None
        self.logger = logging.getLogger(__name__)
        
    def get_next_move(self):
        """
        Decide the next move for the snake
        
        Returns:
            Direction tuple (dx, dy) for next move
        """
        # Replan if dynamic replanning enabled or no current path
        if DYNAMIC_REPLANNING or not self.current_path:
            self._plan_path()
        
        # If path exists and is valid, follow it
        if self.current_path and len(self.current_path) > 1:
            next_pos = self.current_path[1]  # [0] is current position
            head = self.game.snake[0]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            
            # Remove visited position
            self.current_path.pop(0)
            
            return direction
        
        # Fallback: try tail-chasing
        return self._tail_chase_fallback()
    
    def _plan_path(self):
        """Plan path from snake head to food using selected algorithm"""
        head = self.game.snake[0]
        food = self.game.food
        obstacles = set(self.game.snake[1:])  # Body is obstacle, not head
        
        # Choose search algorithm
        if self.algorithm == 'bfs':
            self.search_result = bfs_search(
                head, food, obstacles,
                self.game.grid_rows, self.game.grid_cols
            )
        else:  # astar
            self.search_result = astar_search(
                head, food, obstacles,
                self.game.grid_rows, self.game.grid_cols,
                self.heuristic
            )
        
        # Log search results
        if self.search_result.found:
            self.logger.info(
                f"{self.algorithm.upper()} found path: "
                f"length={len(self.search_result.path)}, "
                f"nodes_expanded={self.search_result.nodes_expanded}"
            )
            
            # Verify path doesn't cause self-collision
            if simulate_snake_movement(self.game.snake, self.search_result.path):
                self.current_path = self.search_result.path
            else:
                self.logger.warning("Path would cause self-collision, using fallback")
                self.current_path = []
        else:
            self.logger.warning(f"No path found to food, using fallback")
            self.current_path = []
    
    def _tail_chase_fallback(self):
        """
        Fallback strategy: chase own tail to buy time
        Moves towards the tail to create space and wait for food access
        
        Returns:
            Direction tuple (dx, dy)
        """
        head = self.game.snake[0]
        tail = self.game.snake[-1]
        
        # Try to path to tail
        obstacles = set(self.game.snake[1:-1])  # Exclude head and tail
        
        search_result = astar_search(
            head, tail, obstacles,
            self.game.grid_rows, self.game.grid_cols,
            'manhattan'
        )
        
        if search_result.found and len(search_result.path) > 1:
            next_pos = search_result.path[1]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            self.logger.info("Using tail-chase strategy")
            return direction
        
        # Last resort: find any safe move
        return self._find_safe_move()
    
    def _find_safe_move(self):
        """
        Find any safe move (last resort)
        
        Returns:
            Direction tuple (dx, dy) or current direction if no safe move
        """
        head = self.game.snake[0]
        safe_neighbors = []
        
        for neighbor in get_neighbors(head, self.game.grid_rows, self.game.grid_cols):
            if self.game.is_position_safe(neighbor):
                safe_neighbors.append(neighbor)
        
        if safe_neighbors:
            # Choose first safe neighbor
            next_pos = safe_neighbors[0]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            self.logger.info("Using safe move fallback")
            return direction
        
        # No safe move available, keep current direction
        self.logger.warning("No safe moves available!")
        return self.game.direction
    
    def get_visualization_data(self):
        """
        Get data for visualizing search process
        
        Returns:
            Dictionary with visited nodes, frontier, and path
        """
        if self.search_result:
            return {
                'visited': self.search_result.visited,
                'frontier': self.search_result.frontier,
                'path': self.current_path
            }
        return {'visited': set(), 'frontier': set(), 'path': []}