"""
Alpha-Beta Pruning AI agent for Snake
Implements minimax with alpha-beta pruning for adversarial search
Models "danger zones" as adversary to avoid traps
"""
import logging
import math
from snake_game.utils import get_neighbors, manhattan_distance


class AlphaBetaAgent:
    """AI agent using Alpha-Beta pruning with minimax"""
    
    def __init__(self, game, max_depth=4):
        """
        Initialize Alpha-Beta agent
        
        Args:
            game: SnakeGame instance
            max_depth: Maximum search depth
        """
        self.game = game
        self.max_depth = max_depth
        self.logger = logging.getLogger(__name__)
        self.nodes_evaluated = 0
    
    def get_next_move(self):
        """
        Decide next move using alpha-beta minimax
        
        Returns:
            Direction tuple (dx, dy)
        """
        head = self.game.snake[0]
        self.nodes_evaluated = 0
        
        # Get all possible moves
        possible_moves = []
        for neighbor in get_neighbors(head, self.game.grid_rows, self.game.grid_cols):
            if self.game.is_position_safe(neighbor):
                direction = (neighbor[0] - head[0], neighbor[1] - head[1])
                possible_moves.append((direction, neighbor))
        
        if not possible_moves:
            return self.game.direction
        
        # Evaluate each move using minimax
        best_move = None
        best_value = -math.inf
        
        for direction, next_pos in possible_moves:
            # Simulate move
            sim_state = self._simulate_move(next_pos)
            
            # Minimax with alpha-beta pruning
            value = self._minimax(sim_state, self.max_depth - 1, -math.inf, math.inf, False)
            
            if value > best_value:
                best_value = value
                best_move = direction
        
        self.logger.info(f"Alpha-Beta: best_value={best_value:.2f}, nodes={self.nodes_evaluated}")
        
        return best_move if best_move else self.game.direction
    
    def _minimax(self, state, depth, alpha, beta, maximizing):
        """
        Minimax algorithm with alpha-beta pruning
        
        Args:
            state: Game state dict
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing: Whether this is a maximizing node
            
        Returns:
            Evaluation score
        """
        self.nodes_evaluated += 1
        
        # Terminal conditions
        if depth == 0 or state['game_over']:
            return self._evaluate_state(state)
        
        head = state['snake'][0]
        
        if maximizing:
            # Maximize: snake tries to improve position
            max_eval = -math.inf
            
            for neighbor in get_neighbors(head, self.game.grid_rows, self.game.grid_cols):
                if self._is_safe_in_state(neighbor, state):
                    new_state = self._simulate_move_from_state(state, neighbor)
                    eval_score = self._minimax(new_state, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    
                    if beta <= alpha:
                        break  # Beta cutoff
            
            return max_eval if max_eval != -math.inf else self._evaluate_state(state)
        
        else:
            # Minimize: "environment" creates danger (e.g., food spawns far, trap opportunities)
            min_eval = math.inf
            
            # Model "adversary" as making the situation worse
            # For snake, this means: less free space, food further, closer to death
            for neighbor in get_neighbors(head, self.game.grid_rows, self.game.grid_cols):
                if self._is_safe_in_state(neighbor, state):
                    new_state = self._simulate_move_from_state(state, neighbor)
                    # Penalize state by adding danger
                    eval_score = self._minimax(new_state, depth - 1, alpha, beta, True) - 5
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    
                    if beta <= alpha:
                        break  # Alpha cutoff
            
            return min_eval if min_eval != math.inf else self._evaluate_state(state)
    
    def _evaluate_state(self, state):
        """
        Heuristic evaluation function for game state
        
        Args:
            state: Game state dict
            
        Returns:
            Evaluation score (higher is better)
        """
        if state['game_over']:
            return -10000
        
        head = state['snake'][0]
        food = state['food']
        snake_length = len(state['snake'])
        
        # Distance to food (negative because closer is better)
        food_dist = manhattan_distance(head, food)
        food_score = -food_dist * 10
        
        # Free space around head (more is better)
        free_space = self._count_free_space(head, state)
        space_score = free_space * 15
        
        # Distance to tail (further is better, creates escape routes)
        if len(state['snake']) > 1:
            tail = state['snake'][-1]
            tail_dist = manhattan_distance(head, tail)
            tail_score = tail_dist * 5
        else:
            tail_score = 0
        
        # Center preference (being in center gives more options)
        center = (self.game.grid_cols // 2, self.game.grid_rows // 2)
        center_dist = manhattan_distance(head, center)
        center_score = -center_dist * 2
        
        # Length bonus
        length_score = snake_length * 20
        
        total_score = food_score + space_score + tail_score + center_score + length_score
        
        return total_score
    
    def _count_free_space(self, pos, state, max_depth=8):
        """
        Count reachable free spaces using flood fill
        
        Args:
            pos: Starting position
            state: Game state
            max_depth: Maximum flood fill depth
            
        Returns:
            Count of reachable free cells
        """
        visited = set()
        queue = [(pos, 0)]
        visited.add(pos)
        obstacles = set(state['snake'][1:])
        
        while queue:
            current, depth = queue.pop(0)
            
            if depth >= max_depth:
                continue
            
            for neighbor in get_neighbors(current, self.game.grid_rows, self.game.grid_cols):
                if neighbor not in visited and neighbor not in obstacles:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        
        return len(visited)
    
    def _simulate_move(self, next_pos):
        """Simulate a move and return new state"""
        new_snake = [next_pos] + self.game.snake[:-1]
        
        # Check if food eaten
        if next_pos == self.game.food:
            new_snake = [next_pos] + self.game.snake  # Grow
        
        # Check game over
        game_over = (
            next_pos in self.game.snake or
            not (0 <= next_pos[0] < self.game.grid_cols and 
                 0 <= next_pos[1] < self.game.grid_rows)
        )
        
        return {
            'snake': new_snake,
            'food': self.game.food,
            'game_over': game_over
        }
    
    def _simulate_move_from_state(self, state, next_pos):
        """Simulate move from existing state"""
        new_snake = [next_pos] + state['snake'][:-1]
        # Check if food eaten
        if next_pos == state['food']:
            new_snake = [next_pos] + state['snake']  # Grow
    
    # Check game over
        game_over = (
            next_pos in state['snake'] or
            not (0 <= next_pos[0] < self.game.grid_cols and 
             0 <= next_pos[1] < self.game.grid_rows)
        )
    
        return {
            'snake': new_snake,
            'food': state['food'],
            'game_over': game_over
        }

def _is_safe_in_state(self, pos, state):
    """Check if position is safe in given state"""
    x, y = pos
    if not (0 <= x < self.game.grid_cols and 0 <= y < self.game.grid_rows):
        return False
    if pos in state['snake'][1:]:
        return False
    return True

def get_visualization_data(self):
    """Get visualization data"""
    return {
        'visited': set(),
        'frontier': set(),
        'path': []
    }