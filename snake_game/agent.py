"""
AI Agent Controller - UPDATED
Now includes survival mode for high scores
CHANGELOG: Added Hamiltonian fallback and survival strategies
"""
import logging
from snake_game.search import astar_search, bfs_search, simulate_snake_movement
from snake_game.config import config
from snake_game.utils import get_neighbors, manhattan_distance


class SnakeAIAgent:
    """AI agent with survival mode for high scores"""
    
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
        self.last_path_length = 0
    
    def get_next_move(self):
        """
        Decide the next move for the snake
        UPDATED: Includes survival mode logic
        
        Returns:
            Direction tuple (dx, dy) for next move
        """
        # Check if in survival mode
        if self.game.survival_mode:
            return self._survival_strategy()
        
        # Replan if dynamic replanning enabled or no current path
        if config.get('ai', 'dynamic_replanning') or not self.current_path:
            self._plan_path()
        
        # If path exists and is valid, follow it
        if self.current_path and len(self.current_path) > 1:
            next_pos = self.current_path[1]
            head = self.game.snake[0]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            
            # Validate move is safe
            if self.game.is_position_safe(next_pos):
                self.current_path.pop(0)
                return direction
        
        # Fallback: try tail-chasing
        return self._tail_chase_fallback()
    
    def _survival_strategy(self):
        """
        Advanced survival strategy for large snakes
        Uses longest path heuristic to avoid trapping
        
        Returns:
            Direction tuple
        """
        head = self.game.snake[0]
        
        # Try to reach food with safety check
        if self._is_food_reachable_safely():
            self._plan_path()
            if self.current_path and len(self.current_path) > 1:
                next_pos = self.current_path[1]
                if self._verify_move_safety(next_pos):
                    direction = (next_pos[0] - head[0], next_pos[1] - head[1])
                    self.current_path.pop(0)
                    return direction
        
        # Otherwise, follow tail to create space
        return self._hamiltonian_fallback()
    
    def _is_food_reachable_safely(self):
        """
        Check if food is reachable and path doesn't trap snake
        
        Returns:
            True if food is safe to pursue
        """
        head = self.game.snake[0]
        food = self.game.food
        
        # Try to find path to food
        obstacles = set(self.game.snake[1:])
        
        if self.algorithm == 'bfs':
            result = bfs_search(head, food, obstacles, 
                              self.game.grid_rows, self.game.grid_cols)
        else:
            result = astar_search(head, food, obstacles,
                                self.game.grid_rows, self.game.grid_cols,
                                self.heuristic)
        
        if not result.found:
            return False
        
        # Simulate eating food and check if tail is still reachable
        sim_snake = [food] + self.game.snake  # Grow snake at food
        sim_head = food
        sim_tail = sim_snake[-1]
        sim_obstacles = set(sim_snake[1:-1])
        
        # Can we reach tail after eating?
        tail_result = astar_search(sim_head, sim_tail, sim_obstacles,
                                  self.game.grid_rows, self.game.grid_cols,
                                  'manhattan')
        
        return tail_result.found
    
    def _verify_move_safety(self, next_pos):
        """
        Verify that a move won't trap the snake
        
        Args:
            next_pos: Proposed next position
            
        Returns:
            True if move is safe
        """
        # Simulate the move
        sim_snake = [next_pos] + self.game.snake[:-1]
        
        # Count reachable spaces from new position
        reachable = self._count_reachable_spaces(next_pos, set(sim_snake[1:]))
        
        # Need at least as much space as current snake length + buffer
        required_space = len(self.game.snake) + 5
        
        return reachable >= required_space
    
    def _count_reachable_spaces(self, start, obstacles, max_depth=None):
        """
        Count reachable empty spaces using flood fill
        
        Args:
            start: Starting position
            obstacles: Set of obstacle positions
            max_depth: Optional depth limit
            
        Returns:
            Number of reachable cells
        """
        visited = {start}
        queue = [(start, 0)]
        
        while queue:
            pos, depth = queue.pop(0)
            
            if max_depth and depth >= max_depth:
                continue
            
            for neighbor in get_neighbors(pos, self.game.grid_rows, self.game.grid_cols):
                if neighbor not in visited and neighbor not in obstacles:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        
        return len(visited)
    
    def _hamiltonian_fallback(self):
        """
        Follow a Hamiltonian-like path by chasing tail
        Creates a cycle that covers the grid
        
        Returns:
            Direction tuple
        """
        head = self.game.snake[0]
        tail = self.game.snake[-1]
        obstacles = set(self.game.snake[1:-1])
        
        # Path to tail
        result = astar_search(head, tail, obstacles,
                            self.game.grid_rows, self.game.grid_cols,
                            'manhattan')
        
        if result.found and len(result.path) > 1:
            next_pos = result.path[1]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            self.logger.info("Using Hamiltonian fallback (tail chase)")
            return direction
        
        # Last resort: any safe move
        return self._find_safe_move()
    
    def _plan_path(self):
        """Plan path from snake head to food using selected algorithm"""
        head = self.game.snake[0]
        food = self.game.food
        obstacles = set(self.game.snake[1:])
        
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
                self.last_path_length = len(self.search_result.path)
            else:
                self.logger.warning("Path would cause self-collision, using fallback")
                self.current_path = []
        else:
            self.logger.warning(f"No path found to food")
            self.current_path = []
    
    def _tail_chase_fallback(self):
        """
        Fallback strategy: chase own tail to buy time
        
        Returns:
            Direction tuple (dx, dy)
        """
        head = self.game.snake[0]
        tail = self.game.snake[-1]
        
        # Try to path to tail
        obstacles = set(self.game.snake[1:-1])
        
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
        safe_neighbors = self.game.get_safe_neighbors(head)
        
        if safe_neighbors:
            # Prefer moves that maximize free space
            best_neighbor = max(
                safe_neighbors,
                key=lambda n: self._count_reachable_spaces(n, set(self.game.snake))
            )
            direction = (best_neighbor[0] - head[0], best_neighbor[1] - head[1])
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