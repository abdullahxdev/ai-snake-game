"""
Pygame renderer for Snake game
Handles all visual rendering including game state and AI visualization
"""
import pygame
from snake_game.config import (
    CELL_SIZE, DARK_THEME, LIGHT_THEME, SHOW_SEARCH_VISUALIZATION
)


class GameRenderer:
    """Handles all game rendering with Pygame"""
    
    def __init__(self, grid_rows, grid_cols, theme='dark'):
        """
        Initialize renderer
        
        Args:
            grid_rows: Number of grid rows
            grid_cols: Number of grid columns
            theme: 'dark' or 'light'
        """
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.cell_size = CELL_SIZE
        self.theme_name = theme
        self.colors = DARK_THEME if theme == 'dark' else LIGHT_THEME
        
        # Calculate window size
        self.width = grid_cols * CELL_SIZE
        self.height = grid_rows * CELL_SIZE + 100  # Extra space for UI
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake AI Game')
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.show_search_viz = SHOW_SEARCH_VISUALIZATION
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.theme_name = 'light' if self.theme_name == 'dark' else 'dark'
        self.colors = DARK_THEME if self.theme_name == 'dark' else LIGHT_THEME
    
    def toggle_search_visualization(self):
        """Toggle search visualization on/off"""
        self.show_search_viz = not self.show_search_viz
    
    def render(self, game_state, ai_data=None, mode='human', algorithm=None):
        """
        Render the game state
        
        Args:
            game_state: Dictionary from game.get_state()
            ai_data: Optional AI visualization data
            mode: 'human' or 'ai'
            algorithm: Current AI algorithm name
        """
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Draw grid
        self._draw_grid()
        
        # Draw AI visualization if enabled
        if ai_data and self.show_search_viz:
            self._draw_ai_visualization(ai_data)
        
        # Draw food
        self._draw_food(game_state['food'])
        
        # Draw snake
        self._draw_snake(game_state['snake'])
        
        # Draw UI
        self._draw_ui(game_state, mode, algorithm)
        
        # Update display
        pygame.display.flip()
    
    def _draw_grid(self):
        """Draw grid lines"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, self.colors['grid'],
                (x, 0), (x, self.grid_rows * self.cell_size)
            )
        
        for y in range(0, self.grid_rows * self.cell_size, self.cell_size):
            pygame.draw.line(
                self.screen, self.colors['grid'],
                (0, y), (self.width, y)
            )
    
    def _draw_snake(self, snake):
        """Draw the snake"""
        for i, (x, y) in enumerate(snake):
            color = self.colors['snake_head'] if i == 0 else self.colors['snake_body']
            rect = pygame.Rect(
                x * self.cell_size + 2,
                y * self.cell_size + 2,
                self.cell_size - 4,
                self.cell_size - 4
            )
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
    
    def _draw_food(self, food):
        """Draw the food"""
        x, y = food
        center = (
            x * self.cell_size + self.cell_size // 2,
            y * self.cell_size + self.cell_size // 2
        )
        pygame.draw.circle(self.screen, self.colors['food'], center, self.cell_size // 3)
    
    def _draw_ai_visualization(self, ai_data):
        """Draw AI search visualization"""
        # Draw visited nodes
        for x, y in ai_data.get('visited', set()):
            rect = pygame.Rect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, self.colors['visited'], rect)
        
        # Draw frontier nodes
        for x, y in ai_data.get('frontier', set()):
            rect = pygame.Rect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, self.colors['frontier'], rect)
        
        # Draw planned path
        path = ai_data.get('path', [])
        if len(path) > 1:
            for i in range(len(path) - 1):
                start = (
                    path[i][0] * self.cell_size + self.cell_size // 2,
                    path[i][1] * self.cell_size + self.cell_size // 2
                )
                end = (
                    path[i + 1][0] * self.cell_size + self.cell_size // 2,
                    path[i + 1][1] * self.cell_size + self.cell_size // 2
                )
                pygame.draw.line(self.screen, self.colors['path'], start, end, 3)
    
    def _draw_ui(self, game_state, mode, algorithm):
        """Draw UI elements (score, controls, etc.)"""
        ui_y = self.grid_rows * self.cell_size + 10
        
        # Score
        score_text = self.font_large.render(
            f"Score: {game_state['score']}  Moves: {game_state['moves']}",
            True, self.colors['text']
        )
        self.screen.blit(score_text, (10, ui_y))
        
        # Mode and algorithm
        mode_text = self.font_small.render(
            f"Mode: {mode.upper()}  |  Algorithm: {algorithm or 'N/A'}  |  Theme: {self.theme_name.upper()}",
            True, self.colors['text']
        )
        self.screen.blit(mode_text, (10, ui_y + 40))
        
        # Controls hint
        controls_text = self.font_small.render(
            "Space: Pause | R: Restart | T: Theme | V: Viz | M: Mode | A: Algorithm | +/-: Speed",
            True, self.colors['text']
        )
        self.screen.blit(controls_text, (10, ui_y + 65))
        
        # Game over message
        if game_state['game_over']:
            game_over_text = self.font_large.render(
                "GAME OVER - Press R to Restart",
                True, self.colors['food']
            )
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            
            # Draw background for text
            bg_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(self.screen, self.colors['background'], bg_rect)
            pygame.draw.rect(self.screen, self.colors['text'], bg_rect, 2)
            
            self.screen.blit(game_over_text, text_rect)
    
    def render_menu(self, fps, paused):
        """
        Render pause menu overlay
        
        Args:
            fps: Current FPS setting
            paused: Whether game is paused
        """
        if paused:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(200)
            overlay.fill(self.colors['background'])
            self.screen.blit(overlay, (0, 0))
            
            # Pause text
            pause_text = self.font_large.render("PAUSED", True, self.colors['text'])
            text_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.screen.blit(pause_text, text_rect)
            
            # FPS text
            fps_text = self.font_small.render(f"Speed: {fps} FPS", True, self.colors['text'])
            fps_rect = fps_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(fps_text, fps_rect)
            
            pygame.display.flip()        