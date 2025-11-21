"""
Pygame Renderer - UPDATED
Now includes animated snake eyes, gradient body, and improved visuals
CHANGELOG: Added eye animation, gradient body, improved UI overlay
"""
import pygame
import math
from snake_game.config import config
from snake_game.themes import get_theme


class GameRenderer:
    """Handles all game rendering with enhanced visuals"""
    
    def __init__(self):
        """Initialize renderer with dynamic sizing"""
        self.window_width = config.get('window', 'width')
        self.window_height = config.get('window', 'height')
        
        # Calculate grid dimensions
        self.cell_size, self.grid_rows, self.grid_cols = config.calculate_grid_dimensions()
        
        # Calculate grid offset to center it
        self.grid_width = self.grid_cols * self.cell_size
        self.grid_height = self.grid_rows * self.cell_size
        self.grid_offset_x = (self.window_width - self.grid_width) // 2
        self.grid_offset_y = 20  # Top margin
        
        # Get theme
        theme_name = config.get('visual', 'default_theme')
        self.theme = get_theme(theme_name)
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(config.get('window', 'title'))
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Animation
        self.animation_time = 0
        
        # Settings
        self.show_search_viz = config.get('ai', 'show_visualization')
        self.show_grid = config.get('visual', 'show_grid')
        self.show_eyes = config.get('visual', 'show_eyes')
        self.gradient_body = config.get('visual', 'gradient_body')
            
    def update_theme(self, theme_name):
        """Update renderer theme"""
        self.theme = get_theme(theme_name)
    
    def toggle_search_visualization(self):
        """Toggle search visualization on/off"""
        self.show_search_viz = not self.show_search_viz
        return self.show_search_viz
    
    def render(self, game_state, ai_data=None, mode='human', algorithm=None, dt=0):
        """
        Render the game state
        
        Args:
            game_state: Dictionary from game.get_state()
            ai_data: Optional AI visualization data
            mode: 'human' or 'ai'
            algorithm: Current AI algorithm name
            dt: Delta time for animations
        """
        self.animation_time += dt
        
        # Draw background gradient
        self._draw_gradient_background()
        
        # Draw grid
        if self.show_grid:
            self._draw_grid()
        
        # Draw AI visualization if enabled
        if ai_data and self.show_search_viz and mode != 'human':
            self._draw_ai_visualization(ai_data)
        
        # Draw food with glow
        self._draw_food(game_state['food'])
        
        # Draw snake with gradient and eyes
        self._draw_snake(game_state['snake'], game_state['direction'])
        
        # Draw UI overlay
        self._draw_ui(game_state, mode, algorithm)
        
        # Update display
        pygame.display.flip()
    
    def _draw_gradient_background(self):
        """Draw animated gradient background"""
        for y in range(self.window_height):
            factor = y / self.window_height
            color = self._interpolate_color(
                self.theme['background_gradient_start'],
                self.theme['background_gradient_end'],
                factor
            )
            pygame.draw.line(self.screen, color, (0, y), (self.window_width, y))
    
    def _draw_grid(self):
        """Draw grid lines"""
        for x in range(self.grid_cols + 1):
            start_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y)
            end_pos = (self.grid_offset_x + x * self.cell_size, 
                      self.grid_offset_y + self.grid_height)
            pygame.draw.line(self.screen, self.theme['grid'], start_pos, end_pos, 1)
        
        for y in range(self.grid_rows + 1):
            start_pos = (self.grid_offset_x, self.grid_offset_y + y * self.cell_size)
            end_pos = (self.grid_offset_x + self.grid_width, 
                      self.grid_offset_y + y * self.cell_size)
            pygame.draw.line(self.screen, self.theme['grid'], start_pos, end_pos, 1)
    
    def _draw_snake(self, snake, direction):
        """Draw snake with gradient body and animated eyes"""
        if not snake:
            return
        
        # Draw body with gradient
        for i, (x, y) in enumerate(snake):
            screen_x = self.grid_offset_x + x * self.cell_size
            screen_y = self.grid_offset_y + y * self.cell_size
            
            # Calculate gradient factor
            if self.gradient_body and len(snake) > 1:
                factor = i / (len(snake) - 1)
                color = self._interpolate_color(
                    self.theme['snake_body_start'],
                    self.theme['snake_body_end'],
                    factor
                )
            else:
                color = self.theme['snake_head'] if i == 0 else self.theme['snake_body_start']
            
            # Draw segment with rounded corners
            rect = pygame.Rect(
                screen_x + 2,
                screen_y + 2,
                self.cell_size - 4,
                self.cell_size - 4
            )
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            
            # Draw eyes on head
            if i == 0 and self.show_eyes:
                self._draw_eyes(screen_x, screen_y, direction)
    
    def _draw_eyes(self, x, y, direction):
        """Draw animated eyes on snake head"""
        dx, dy = direction
        
        # Eye positions based on direction
        if dx == 1:  # Right
            eye1_pos = (x + self.cell_size * 0.65, y + self.cell_size * 0.35)
            eye2_pos = (x + self.cell_size * 0.65, y + self.cell_size * 0.65)
            pupil_offset = (3, 0)
        elif dx == -1:  # Left
            eye1_pos = (x + self.cell_size * 0.35, y + self.cell_size * 0.35)
            eye2_pos = (x + self.cell_size * 0.35, y + self.cell_size * 0.65)
            pupil_offset = (-3, 0)
        elif dy == -1:  # Up
            eye1_pos = (x + self.cell_size * 0.35, y + self.cell_size * 0.35)
            eye2_pos = (x + self.cell_size * 0.65, y + self.cell_size * 0.35)
            pupil_offset = (0, -3)
        else:  # Down
            eye1_pos = (x + self.cell_size * 0.35, y + self.cell_size * 0.65)
            eye2_pos = (x + self.cell_size * 0.65, y + self.cell_size * 0.65)
            pupil_offset = (0, 3)
        
        # Draw eyes
        eye_radius = max(3, self.cell_size // 8)
        pupil_radius = max(2, self.cell_size // 12)
        
        # Eye whites
        pygame.draw.circle(self.screen, self.theme['snake_eye'], 
                         (int(eye1_pos[0]), int(eye1_pos[1])), eye_radius)
        pygame.draw.circle(self.screen, self.theme['snake_eye'], 
                         (int(eye2_pos[0]), int(eye2_pos[1])), eye_radius)
        
        # Pupils
        pygame.draw.circle(self.screen, self.theme['snake_pupil'],
                         (int(eye1_pos[0] + pupil_offset[0]), 
                          int(eye1_pos[1] + pupil_offset[1])), pupil_radius)
        pygame.draw.circle(self.screen, self.theme['snake_pupil'],
                         (int(eye2_pos[0] + pupil_offset[0]), 
                          int(eye2_pos[1] + pupil_offset[1])), pupil_radius)
    
    def _draw_food(self, food):
        """Draw food with pulsing glow effect"""
        x, y = food
        screen_x = self.grid_offset_x + x * self.cell_size + self.cell_size // 2
        screen_y = self.grid_offset_y + y * self.cell_size + self.cell_size // 2
        
        # Pulsing glow
        glow_radius = int(self.cell_size * 0.6 + math.sin(self.animation_time * 5) * 3)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*self.theme['food_glow'], 50), 
                         (glow_radius, glow_radius), glow_radius)
        self.screen.blit(glow_surface, 
                        (screen_x - glow_radius, screen_y - glow_radius))
        
        # Food circle
        food_radius = self.cell_size // 3
        pygame.draw.circle(self.screen, self.theme['food'], 
                         (screen_x, screen_y), food_radius)
    
    def _draw_ai_visualization(self, ai_data):
        """Draw AI search visualization"""
        # Draw visited nodes
        for x, y in ai_data.get('visited', set()):
            screen_x = self.grid_offset_x + x * self.cell_size
            screen_y = self.grid_offset_y + y * self.cell_size
            rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.theme['visited'], rect)
        
        # Draw frontier nodes
        for x, y in ai_data.get('frontier', set()):
            screen_x = self.grid_offset_x + x * self.cell_size
            screen_y = self.grid_offset_y + y * self.cell_size
            rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.theme['frontier'], rect)
        
        # Draw planned path
        path = ai_data.get('path', [])
        if len(path) > 1:
            for i in range(len(path) - 1):
                start = (
                    self.grid_offset_x + path[i][0] * self.cell_size + self.cell_size // 2,
                    self.grid_offset_y + path[i][1] * self.cell_size + self.cell_size // 2
                )
                end = (
                    self.grid_offset_x + path[i + 1][0] * self.cell_size + self.cell_size // 2,
                    self.grid_offset_y + path[i + 1][1] * self.cell_size + self.cell_size // 2
                )
                pygame.draw.line(self.screen, self.theme['path'], start, end, 4)
    
    def _draw_ui(self, game_state, mode, algorithm):
        """Draw UI overlay with game info"""
        ui_y = self.grid_offset_y + self.grid_height + 20
        
        # Score and stats
        score_text = self.font_large.render(
            f"Score: {game_state['score']}", True, self.theme['text']
        )
        self.screen.blit(score_text, (20, ui_y))
        
        moves_text = self.font_medium.render(
            f"Moves: {game_state['moves']}", True, self.theme['text']
        )
        self.screen.blit(moves_text, (20, ui_y + 50))
        
        # Mode and algorithm
        mode_text = self.font_medium.render(
            f"Mode: {mode.upper()}", True, self.theme['snake_head']
        )
        self.screen.blit(mode_text, (self.window_width - 300, ui_y))
        
        if mode != 'human' and algorithm:
            algo_text = self.font_small.render(
                f"Algorithm: {algorithm.upper()}", True, self.theme['text']
            )
            self.screen.blit(algo_text, (self.window_width - 300, ui_y + 35))
        
        # Survival mode indicator
        if game_state.get('survival_mode'):
            survival_text = self.font_medium.render(
                "SURVIVAL MODE", True, self.theme['food']
            )
            survival_rect = survival_text.get_rect(center=(self.window_width // 2, ui_y + 25))
            self.screen.blit(survival_text, survival_rect)
        
        # Controls hint
        controls_text = self.font_small.render(
            "ESC: Menu | Space: Pause | R: Restart | V: Viz | +/-: Speed",
            True, self.theme['text']
        )
        self.screen.blit(controls_text, (20, self.window_height - 30))
        
        # Game over message
        if game_state['game_over']:
            self._draw_game_over(game_state['score'])
    
    def _draw_game_over(self, score):
        """Draw game over overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(180)
        overlay.fill(self.theme['background'])
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, self.theme['food'])
        game_over_rect = game_over_text.get_rect(center=(self.window_width // 2, 
                                                         self.window_height // 2 - 40))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {score}", True, self.theme['text'])
        score_rect = score_text.get_rect(center=(self.window_width // 2, 
                                                 self.window_height // 2 + 10))
        self.screen.blit(score_text, score_rect)
        
        # Restart hint
        restart_text = self.font_small.render("Press R to Restart or ESC for Menu", 
                                             True, self.theme['text'])
        restart_rect = restart_text.get_rect(center=(self.window_width // 2, 
                                                     self.window_height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def _interpolate_color(self, color1, color2, factor):
        """Interpolate between two colors"""
        return tuple(
            int(color1[i] + (color2[i] - color1[i]) * factor)
            for i in range(3)  # Assuming RGB color tuple (3 components)
        )


    def render_pause_menu(self, fps):
        """
        Render pause menu overlay

        Args:
            fps: Current FPS setting
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(200)
        overlay.fill(self.theme['background'])
        self.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font_large.render("PAUSED", True, self.theme['text'])
        pause_rect = pause_text.get_rect(center=(self.window_width // 2,
                                                  self.window_height // 2 - 80))
        self.screen.blit(pause_text, pause_rect)

        # FPS text
        fps_text = self.font_medium.render(f"Speed: {fps} FPS", True, self.theme['text'])
        fps_rect = fps_text.get_rect(center=(self.window_width // 2,
                                              self.window_height // 2 - 20))
        self.screen.blit(fps_text, fps_rect)

        # Controls
        controls = [
            "Space: Resume",
            "+/-: Adjust Speed",
            "R: Restart",
            "ESC: Main Menu"
        ]
        y_offset = self.window_height // 2 + 30
        for control in controls:
            text = self.font_small.render(control, True, self.theme['text'])
            text_rect = text.get_rect(center=(self.window_width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30

        pygame.display.flip()