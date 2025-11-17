"""
Performance evaluation for AI agents
Runs multiple games and collects statistics
"""
import time
import statistics
from snake_game.game import SnakeGame
from snake_game.agent import SnakeAIAgent
from snake_game.config import GRID_ROWS, GRID_COLS


class PerformanceEvaluator:
    """Evaluates AI agent performance"""
    
    def __init__(self, num_games=100, max_moves=1000, headless=True):
        """
        Initialize evaluator
        
        Args:
            num_games: Number of games to run
            max_moves: Maximum moves per game
            headless: Run without GUI
        """
        self.num_games = num_games
        self.max_moves = max_moves
        self.headless = headless
    
    def run_single_game(self, algorithm='astar', heuristic='manhattan'):
        """
        Run a single AI game
        
        Args:
            algorithm: 'bfs' or 'astar'
            heuristic: 'manhattan' or 'euclidean'
            
        Returns:
            Dictionary with game statistics
        """
        game = SnakeGame(GRID_ROWS, GRID_COLS)
        agent = SnakeAIAgent(game, algorithm, heuristic)
        
        start_time = time.time()
        moves = 0
        
        while not game.game_over and moves < self.max_moves:
            direction = agent.get_next_move()
            game.change_direction(direction)
            game.update()
            moves += 1
        
        end_time = time.time()
        
        return {
            'score': game.score,
            'moves': moves,
            'game_over': game.game_over,
            'time': end_time - start_time,
            'survival_rate': moves / self.max_moves if not game.game_over else 1.0
        }
    
    def evaluate(self, algorithm='astar', heuristic='manhattan'):
        """
        Run multiple games and collect statistics
        
        Args:
            algorithm: 'bfs' or 'astar'
            heuristic: 'manhattan' or 'euclidean'
            
        Returns:
            Dictionary with aggregate statistics
        """
        print(f"\nRunning {self.num_games} games with {algorithm.upper()} ({heuristic})...")
        
        scores = []
        moves_list = []
        times = []
        failures = 0
        timeouts = 0
        
        for i in range(self.num_games):
            result = self.run_single_game(algorithm, heuristic)
            
            scores.append(result['score'])
            moves_list.append(result['moves'])
            times.append(result['time'])
            
            if result['game_over']:
                failures += 1
            if result['moves'] >= self.max_moves:
                timeouts += 1
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/{self.num_games} games...")
        
        # Calculate statistics
        stats = {
            'algorithm': algorithm,
            'heuristic': heuristic,
            'num_games': self.num_games,
            'avg_score': statistics.mean(scores),
            'max_score': max(scores),
            'min_score': min(scores),
            'std_score': statistics.stdev(scores) if len(scores) > 1 else 0,
            'avg_moves': statistics.mean(moves_list),
            'avg_time': statistics.mean(times),
            'failure_rate': failures / self.num_games,
            'timeout_rate': timeouts / self.num_games,
            'success_rate': (self.num_games - failures) / self.num_games
        }
        
        return stats
    
    def compare_algorithms(self):
        """
        Compare BFS and A* performance
        
        Returns:
            Dictionary with comparison results
        """
        print("\n" + "="*60)
        print("PERFORMANCE COMPARISON: BFS vs A*")
        print("="*60)
        
        # Test both algorithms
        bfs_stats = self.evaluate('bfs', 'manhattan')
        astar_manhattan_stats = self.evaluate('astar', 'manhattan')
        astar_euclidean_stats = self.evaluate('astar', 'euclidean')
        
        # Print results
        self._print_stats("BFS", bfs_stats)
        self._print_stats("A* (Manhattan)", astar_manhattan_stats)
        self._print_stats("A* (Euclidean)", astar_euclidean_stats)
        
        # Winner analysis
        print("\n" + "="*60)
        print("WINNER ANALYSIS")
        print("="*60)
        
        best_avg_score = max(
            bfs_stats['avg_score'],
            astar_manhattan_stats['avg_score'],
            astar_euclidean_stats['avg_score']
        )
        
        if best_avg_score == astar_manhattan_stats['avg_score']:
            print("🏆 Best Average Score: A* (Manhattan)")
        elif best_avg_score == astar_euclidean_stats['avg_score']:
            print("🏆 Best Average Score: A* (Euclidean)")
        else:
            print("🏆 Best Average Score: BFS")
        
        print(f"   Score: {best_avg_score:.2f}")
        
        return {
            'bfs': bfs_stats,
            'astar_manhattan': astar_manhattan_stats,
            'astar_euclidean': astar_euclidean_stats
        }
    
    def _print_stats(self, name, stats):
        """Print statistics in formatted table"""
        print(f"\n{name}:")
        print("-" * 60)
        print(f"  Average Score:     {stats['avg_score']:.2f} ± {stats['std_score']:.2f}")
        print(f"  Max Score:         {stats['max_score']}")
        print(f"  Min Score:         {stats['min_score']}")
        print(f"  Average Moves:     {stats['avg_moves']:.1f}")
        print(f"  Average Time:      {stats['avg_time']:.3f}s per game")
        print(f"  Success Rate:      {stats['success_rate']*100:.1f}%")
        print(f"  Failure Rate:      {stats['failure_rate']*100:.1f}%")
        print(f"  Timeout Rate:      {stats['timeout_rate']*100:.1f}%")


def main():
    """Run performance evaluation"""
    evaluator = PerformanceEvaluator(num_games=50, max_moves=1000)
    results = evaluator.compare_algorithms()
    
    print("\n" + "="*60)
    print("Evaluation complete! Results saved to logs/")
    print("="*60)


if __name__ == '__main__':
    main()