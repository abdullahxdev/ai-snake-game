"""
Search algorithms for AI agent: BFS and A*
Implements pathfinding with visualization support
"""
from collections import deque
import heapq
from snake_game.utils import get_neighbors
from snake_game.heuristics import get_heuristic


class SearchResult:
    """Container for search algorithm results"""
    
    def __init__(self, path=None, visited=None, frontier=None, 
                 nodes_expanded=0, path_cost=0, found=False):
        self.path = path or []
        self.visited = visited or set()
        self.frontier = frontier or set()
        self.nodes_expanded = nodes_expanded
        self.path_cost = path_cost
        self.found = found


def bfs_search(start, goal, obstacles, grid_rows, grid_cols):
    """
    Breadth-First Search algorithm for pathfinding
    
    Args:
        start: Starting position (x, y)
        goal: Goal position (x, y)
        obstacles: Set of obstacle positions
        grid_rows: Number of grid rows
        grid_cols: Number of grid columns
        
    Returns:
        SearchResult object containing path and search statistics
    """
    # Initialize queue with start position
    queue = deque([(start, [start])])
    visited = {start}
    frontier = set()
    nodes_expanded = 0
    
    while queue:
        current, path = queue.popleft()
        nodes_expanded += 1
        
        # Goal check
        if current == goal:
            return SearchResult(
                path=path,
                visited=visited,
                frontier=frontier,
                nodes_expanded=nodes_expanded,
                path_cost=len(path),
                found=True
            )
        
        # Expand neighbors
        for neighbor in get_neighbors(current, grid_rows, grid_cols):
            if neighbor not in visited and neighbor not in obstacles:
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
                frontier.add(neighbor)
        
        # Remove current from frontier
        frontier.discard(current)
    
    # No path found
    return SearchResult(
        visited=visited,
        frontier=frontier,
        nodes_expanded=nodes_expanded,
        found=False
    )


def astar_search(start, goal, obstacles, grid_rows, grid_cols, heuristic_name='manhattan'):
    """
    A* Search algorithm for pathfinding
    
    Args:
        start: Starting position (x, y)
        goal: Goal position (x, y)
        obstacles: Set of obstacle positions
        grid_rows: Number of grid rows
        grid_cols: Number of grid columns
        heuristic_name: Name of heuristic function to use
        
    Returns:
        SearchResult object containing path and search statistics
    """
    heuristic = get_heuristic(heuristic_name)
    
    # Priority queue: (f_score, counter, current, path, g_score)
    # Counter ensures stable sorting for equal f_scores
    counter = 0
    heap = [(heuristic(start, goal), counter, start, [start], 0)]
    visited = set()
    frontier = {start}
    nodes_expanded = 0
    
    # Track best g_score for each position
    g_scores = {start: 0}
    
    while heap:
        f_score, _, current, path, g_score = heapq.heappop(heap)
        
        # Skip if already visited with better path
        if current in visited:
            continue
        
        visited.add(current)
        nodes_expanded += 1
        frontier.discard(current)
        
        # Goal check
        if current == goal:
            return SearchResult(
                path=path,
                visited=visited,
                frontier=frontier,
                nodes_expanded=nodes_expanded,
                path_cost=g_score,
                found=True
            )
        
        # Expand neighbors
        for neighbor in get_neighbors(current, grid_rows, grid_cols):
            if neighbor in visited or neighbor in obstacles:
                continue
            
            # Calculate new g_score (uniform cost = 1 per move)
            new_g_score = g_score + 1
            
            # Only process if this is a better path
            if neighbor not in g_scores or new_g_score < g_scores[neighbor]:
                g_scores[neighbor] = new_g_score
                h_score = heuristic(neighbor, goal)
                new_f_score = new_g_score + h_score
                new_path = path + [neighbor]
                
                counter += 1
                heapq.heappush(heap, (new_f_score, counter, neighbor, new_path, new_g_score))
                frontier.add(neighbor)
    
    # No path found
    return SearchResult(
        visited=visited,
        frontier=frontier,
        nodes_expanded=nodes_expanded,
        found=False
    )


def simulate_snake_movement(snake_body, path):
    """
    Simulate snake movement along a path to check for self-collision
    
    Args:
        snake_body: List of current snake body positions
        path: Proposed path to follow
        
    Returns:
        True if path is safe, False if self-collision would occur
    """
    # Create a copy of the snake body
    sim_snake = list(snake_body)
    
    # Simulate each move in the path
    for next_pos in path[1:]:  # Skip current head position
        sim_snake.insert(0, next_pos)  # Add new head
        sim_snake.pop()  # Remove tail (no growth during simulation)
        
        # Check for self-collision
        if next_pos in sim_snake[1:]:
            return False
    
    return True