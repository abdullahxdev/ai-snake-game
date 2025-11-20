"""
Main Game Controller - COMPLETELY UPDATED
Now includes menu system, multiple AI modes, and improved game flow
CHANGELOG: Complete rewrite with menu integration, theme system, audio
"""
import pygame
import sys
import time
from snake_game.game import SnakeGame
from snake_game.renderer import GameRenderer
from snake_game.agent import SnakeAIAgent
from snake_game.agent_bfs import BFSAgent
from snake_game.agent_alphabeta import AlphaBetaAgent
from snake_game.config import config
from snake_game.audio import AudioManager
from snake_game.ui.menu import MainMenu, SettingsMenu, ModeMenu
from snake_game.utils import setup_logging


class GameController:
    """Main game controller with menu system"""
    
    def __init__(self, headless=False):
        """
        Initialize game controller
        
        Args:
            headless: Run without GUI for benchmarking
        """
        self.headless = headless or config.get('performance', 'headless_mode')
        
        # Initialize components
        self.game = SnakeGame()
        self.renderer = GameRenderer() if not self.headless else None
        self.audio = AudioManager(
            enabled=config.get('audio', 'enabled'),
            volume=config.get('audio', 'volume')
        )
        
        # Game state
        self.mode = config.get('ai', 'default_mode')
        self.algorithm = config.get('ai', 'default_mode') if self.mode != 'human' else 'astar'
        self.fps = config.get('game', 'default_fps')
        self.paused = False
        self.clock = pygame.time.Clock()
        self._game_over_played = False
        
        # AI agent
        self.agent = None
        if self.mode != 'human':
            self._create_agent()
        
        # Menu system
        window_width = config.get('window', 'width')
        window_height = config.get('window', 'height')
        
        self.main_menu = MainMenu(window_width, window_height, config, self.audio)
        self.settings_menu = SettingsMenu(window_width, window_height, config, self.audio)
        self.mode_menu = ModeMenu(window_width, window_height, config, self.audio)
        
        # State management
        self.state = 'menu'  # 'menu', 'game', 'settings', 'mode_select'
        self.transition_alpha = 0
        self.transitioning = False
        
        # Setup logging
        self.logger = setup_logging()
        
        if self.logger:
            self.logger.info("Game controller initialized")
    
    def _create_agent(self):
        """Create AI agent based on current mode"""
        if self.mode == 'human':
            self.agent = None
        elif self.mode == 'bfs':
            self.agent = BFSAgent(self.game)
        elif self.mode == 'alphabeta':
            depth = config.get('ai', 'alphabeta_depth')
            self.agent = AlphaBetaAgent(self.game, max_depth=depth)
        else:  # astar
            heuristic = config.get('ai', 'heuristic')
            self.agent = SnakeAIAgent(self.game, 'astar', heuristic)
    
    def run(self):
        """Main game loop"""
        if self.logger:
            self.logger.info("Game started")
        
        running = True
        last_time = time.time()
        
        while running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if self.state == 'menu':
                        self.main_menu.handle_event(event)
                    elif self.state == 'settings':
                        self.settings_menu.handle_event(event)
                    elif self.state == 'mode_select':
                        self.mode_menu.handle_event(event)
                    elif self.state == 'game':
                        self._handle_game_event(event)
            
            # Update based on state
            if self.state == 'menu':
                self._update_menu(dt)
            elif self.state == 'settings':
                self._update_settings(dt)
            elif self.state == 'mode_select':
                self._update_mode_menu(dt)
            elif self.state == 'game':
                self._update_game(dt)
            
            # Render based on state
            if not self.headless and self.renderer:
                if self.state == 'menu':
                    self.main_menu.draw(self.renderer.screen)
                elif self.state == 'settings':
                    self.settings_menu.draw(self.renderer.screen)
                elif self.state == 'mode_select':
                    self.mode_menu.draw(self.renderer.screen)
                elif self.state == 'game':
                    self._render_game(dt)
                
                pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(60 if self.state != 'game' else self.fps)
        
        # Cleanup
        self._cleanup()
    
    def _update_menu(self, dt):
        """Update main menu"""
        self.main_menu.update(dt)
        
        action = self.main_menu.get_action()
        if action == 'play':
            self.audio.play('transition')
            self._transition_to_game()
        elif action == 'settings':
            self.state = 'settings'
        elif action == 'mode':
            self.state = 'mode_select'
        elif action == 'quit':
            pygame.quit()
            sys.exit()
    
    def _update_settings(self, dt):
        """Update settings menu"""
        self.settings_menu.update(dt)
        
        action = self.settings_menu.get_action()
        if action == 'back':
            # Update renderer theme
            theme_name = config.get('visual', 'default_theme')
            if self.renderer:
                self.renderer.update_theme(theme_name)
            self.main_menu.update_theme(theme_name)
            self.mode_menu.update_theme(theme_name)
            
            # Update FPS
            self.fps = config.get('game', 'default_fps')
            
            self.state = 'menu'
    
    def _update_mode_menu(self, dt):
        """Update mode selection menu"""
        self.mode_menu.update(dt)
        
        action = self.mode_menu.get_action()
        if action == 'back':
            # Update mode
            self.mode = config.get('ai', 'default_mode')
            self.state = 'menu'
    
    def _transition_to_game(self):
        """Transition from menu to game"""
        self.game.reset()
        self.mode = config.get('ai', 'default_mode')
        self._create_agent()
        self.paused = False
        self.state = 'game'
        self._game_over_played = False
        
        if self.logger:
            self.logger.info(f"Starting game in {self.mode} mode")
    
    def _handle_game_event(self, event):
        """Handle game input events"""
        if event.type == pygame.KEYDOWN:
            # Game controls
            if event.key == pygame.K_ESCAPE:
                self.audio.play('click')
                self.state = 'menu'
            
            elif event.key == pygame.K_SPACE:
                self.paused = not self.paused
                self.audio.play('click')
            
            elif event.key == pygame.K_r:
                self.game.reset()
                self._create_agent()
                self.audio.play('click')
                self._game_over_played = False
            
            elif event.key == pygame.K_v:
                if self.renderer:
                    viz_state = self.renderer.toggle_search_visualization()
                    self.audio.play('click')
                    if self.logger:
                        self.logger.info(f"Visualization: {'ON' if viz_state else 'OFF'}")
            
            elif event.key in [pygame.K_PLUS, pygame.K_EQUALS]:
                self._adjust_speed(1)
            
            elif event.key == pygame.K_MINUS:
                self._adjust_speed(-1)
            
            # Human player controls
            elif self.mode == 'human' and not self.paused:
                if event.key == pygame.K_UP:
                    self.game.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.game.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.game.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.game.change_direction((1, 0))
    
    def _adjust_speed(self, delta):
        """Adjust game speed"""
        min_fps = config.get('game', 'min_fps')
        max_fps = config.get('game', 'max_fps')
        self.fps = max(min_fps, min(max_fps, self.fps + delta))
        self.audio.play('click')
        
        if self.logger:
            self.logger.info(f"Speed adjusted to: {self.fps} FPS")
    
    def _update_game(self, dt):
        """Update game state"""
        if self.paused:
            return
        
        # AI decision
        if self.mode != 'human' and not self.game.game_over:
            direction = self.agent.get_next_move()
            self.game.change_direction(direction)
        
        # Update game
        if not self.game.game_over:
            # Store previous score
            prev_score = self.game.score
            
            # Update
            self.game.update()
            
            # Check if food was eaten
            if self.game.score > prev_score:
                self.audio.play('eat')
    
    def _render_game(self, dt):
        """Render game state"""
        if self.paused:
            self.renderer.render_pause_menu(self.fps)
        else:
            ai_data = None
            if self.mode != 'human' and self.agent:
                ai_data = self.agent.get_visualization_data()
            
            self.renderer.render(
                self.game.get_state(),
                ai_data=ai_data,
                mode=self.mode,
                algorithm=self.algorithm,
                dt=dt
            )
        
        # Play game over sound once
        if self.game.game_over and not self._game_over_played:
            self.audio.play('gameover')
            self._game_over_played = True
    
    def _cleanup(self):
        """Cleanup before exit"""
        if self.logger:
            final_state = self.game.get_state()
            self.logger.info(
                f"Game ended - Score: {final_state['score']}, "
                f"Moves: {final_state['moves']}, Mode: {self.mode}"
            )
        
        config.save()
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Snake AI Game')
    parser.add_argument('--headless', action='store_true', 
                       help='Run without GUI for benchmarking')
    args = parser.parse_args()
    
    controller = GameController(headless=args.headless)
    controller.run()


if __name__ == '__main__':
    main()