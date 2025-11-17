"""
Main entry point for Snake AI Game
Handles game loop, input, and mode switching
"""
import pygame
import sys
from snake_game.game import SnakeGame
from snake_game.renderer import GameRenderer
from snake_game.agent import SnakeAIAgent
from snake_game.config import (
    GRID_ROWS, GRID_COLS, DEFAULT_FPS, MIN_FPS, MAX_FPS,
    UP, DOWN, LEFT, RIGHT, AI_ALGORITHM, AI_HEURISTIC
)
from snake_game.utils import setup_logging


class GameController:
    """Main game controller handling game loop and user input"""
    
    def __init__(self):
        """Initialize game controller"""
        self.game = SnakeGame(GRID_ROWS, GRID_COLS)
        self.renderer = GameRenderer(GRID_ROWS, GRID_COLS)
        self.agent = None
        
        self.mode = 'human'  # 'human' or 'ai'
        self.algorithm = AI_ALGORITHM
        self.heuristic = AI_HEURISTIC
        self.fps = DEFAULT_FPS
        self.paused = False
        self.clock = pygame.time.Clock()
        
        # Setup logging
        self.logger = setup_logging()
        
    def toggle_mode(self):
        """Toggle between human and AI mode"""
        self.mode = 'ai' if self.mode == 'human' else 'human'
        
        if self.mode == 'ai' and self.agent is None:
            self.agent = SnakeAIAgent(self.game, self.algorithm, self.heuristic)
            if self.logger:
                self.logger.info(f"AI mode activated: {self.algorithm}, {self.heuristic}")
        
        if self.logger:
            self.logger.info(f"Mode switched to: {self.mode}")
    
    def toggle_algorithm(self):
        """Toggle between BFS and A* algorithms"""
        if self.mode == 'ai':
            self.algorithm = 'bfs' if self.algorithm == 'astar' else 'astar'
            self.agent = SnakeAIAgent(self.game, self.algorithm, self.heuristic)
            
            if self.logger:
                self.logger.info(f"Algorithm switched to: {self.algorithm}")
    
    def adjust_speed(self, delta):
        """
        Adjust game speed
        
        Args:
            delta: Speed change (+1 or -1)
        """
        self.fps = max(MIN_FPS, min(MAX_FPS, self.fps + delta))
        
        if self.logger:
            self.logger.info(f"Speed adjusted to: {self.fps} FPS")
    
    def handle_input(self):
        """
        Handle keyboard input
        
        Returns:
            False if quit requested, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # Game controls
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                
                elif event.key == pygame.K_r:
                    self.game.reset()
                    if self.mode == 'ai':
                        self.agent = SnakeAIAgent(self.game, self.algorithm, self.heuristic)
                
                elif event.key == pygame.K_t:
                    self.renderer.toggle_theme()
                
                elif event.key == pygame.K_v:
                    self.renderer.toggle_search_visualization()
                
                elif event.key == pygame.K_m:
                    self.toggle_mode()
                
                elif event.key == pygame.K_a:
                    self.toggle_algorithm()
                
                elif event.key in [pygame.K_PLUS, pygame.K_EQUALS]:
                    self.adjust_speed(1)
                
                elif event.key == pygame.K_MINUS:
                    self.adjust_speed(-1)
                
                # The controls for the human player
                elif self.mode == 'human' and not self.paused:
                    if event.key == pygame.K_UP:
                        self.game.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.game.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.game.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.game.change_direction(RIGHT)
        
        return True
    
    def run(self):
        """Main game loop"""
        running = True
        
        if self.logger:
            self.logger.info("Game started")
        
        while running:
            # Handle input
            running = self.handle_input()
            
            if self.paused:
                self.renderer.render_menu(self.fps, self.paused)
                self.clock.tick(30)  # Lower FPS when paused
                continue
            
            # AI decision
            ai_data = None
            if self.mode == 'ai' and not self.game.game_over:
                direction = self.agent.get_next_move()
                self.game.change_direction(direction)
                ai_data = self.agent.get_visualization_data()
            
            # Update game
            if not self.game.game_over:
                self.game.update()
            
            # Render
            self.renderer.render(
                self.game.get_state(),
                ai_data=ai_data,
                mode=self.mode,
                algorithm=self.algorithm if self.mode == 'ai' else None
            )
            
            # Control frame rate
            self.clock.tick(self.fps)
        
        # Cleanup
        if self.logger:
            final_state = self.game.get_state()
            self.logger.info(
                f"Game ended - Score: {final_state['score']}, "
                f"Moves: {final_state['moves']}, Mode: {self.mode}"
            )
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game"""
    controller = GameController()
    controller.run()


if __name__ == '__main__':
    main()