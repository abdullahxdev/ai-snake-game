"""
Main menu and settings screens
"""
import pygame
import random
import math
from snake_game.ui.button import Button, Slider, Toggle
from snake_game.themes import get_theme


class GhostSnake:
    """Animated background snake for menu"""
    
    def __init__(self, x, y, length, speed, color, grid_rows, grid_cols):
        """Initialize ghost snake"""
        self.body = [(x, y)]
        self.target_length = length
        self.speed = speed
        self.color = color
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.move_timer = 0
        
        # Grow to target length
        for _ in range(length - 1):
            self.body.append(self.body[-1])
    
    def update(self, dt):
        """Update ghost snake position"""
        self.move_timer += dt
        
        if self.move_timer >= self.speed:
            self.move_timer = 0
            
            # Randomly change direction
            if random.random() < 0.1:
                self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            
            # Calculate new head position
            head = self.body[0]
            new_head = (
                (head[0] + self.direction[0]) % self.grid_cols,
                (head[1] + self.direction[1]) % self.grid_rows
            )
            
            # Move
            self.body.insert(0, new_head)
            if len(self.body) > self.target_length:
                self.body.pop()
    
    def draw(self, surface, cell_size, offset_x, offset_y, alpha=100):
        """Draw ghost snake with transparency"""
        for i, (x, y) in enumerate(self.body):
            # Create semi-transparent surface
            segment_surface = pygame.Surface((cell_size - 4, cell_size - 4))
            segment_surface.set_alpha(alpha)
            segment_surface.fill(self.color)
            
            pos = (x * cell_size + offset_x + 2, y * cell_size + offset_y + 2)
            surface.blit(segment_surface, pos)


class MainMenu:
    """Main menu screen with animated background"""
    
    def __init__(self, width, height, config, audio_manager):
        """
        Initialize main menu
        
        Args:
            width: Screen width
            height: Screen height
            config: ConfigManager instance
            audio_manager: AudioManager instance
        """
        self.width = width
        self.height = height
        self.config = config
        self.audio = audio_manager
        
        # Get theme
        theme_name = config.get('visual', 'default_theme')
        self.theme = get_theme(theme_name)
        
        # Calculate grid for background
        self.cell_size = 30
        self.grid_cols = width // self.cell_size
        self.grid_rows = height // self.cell_size
        
        # Create ghost snakes
        self.ghost_snakes = []
        num_ghosts = config.get('menu', 'ghost_snakes')
        colors = [
            self.theme['snake_body_start'],
            self.theme['snake_body_end'],
            self.theme['visited'],
            self.theme['frontier']
        ]
        
        for i in range(num_ghosts):
            x = random.randint(0, self.grid_cols - 1)
            y = random.randint(0, self.grid_rows - 1)
            length = random.randint(10, 20)
            speed = random.uniform(0.1, 0.3)
            color = colors[i % len(colors)]
            
            ghost = GhostSnake(x, y, length, speed, color, self.grid_rows, self.grid_cols)
            self.ghost_snakes.append(ghost)
        
        # Gradient animation
        self.gradient_offset = 0
        
        # Create buttons
        button_width = 300
        button_height = 60
        button_x = (width - button_width) // 2
        start_y = height // 2 - 50
        spacing = 80
        
        self.buttons = []
        
        self.play_button = Button(
            button_x, start_y, button_width, button_height,
            "PLAY", self.theme, on_click=self.on_play
        )
        self.buttons.append(self.play_button)
        
        self.settings_button = Button(
            button_x, start_y + spacing, button_width, button_height,
            "SETTINGS", self.theme, on_click=self.on_settings
        )
        self.buttons.append(self.settings_button)
        
        self.mode_button = Button(
            button_x, start_y + spacing * 2, button_width, button_height,
            "MODE", self.theme, on_click=self.on_mode
        )
        self.buttons.append(self.mode_button)
        
        self.quit_button = Button(
            button_x, start_y + spacing * 3, button_width, button_height,
            "QUIT", self.theme, on_click=self.on_quit
        )
        self.buttons.append(self.quit_button)
        
        # Title font
        self.title_font = pygame.font.Font(None, 100)
        self.subtitle_font = pygame.font.Font(None, 36)
        
        # Menu state
        self.action = None
    
    def on_play(self):
        """Play button clicked"""
        self.audio.play('click')
        self.action = 'play'
    
    def on_settings(self):
        """Settings button clicked"""
        self.audio.play('click')
        self.action = 'settings'
    
    def on_mode(self):
        """Mode button clicked"""
        self.audio.play('click')
        self.action = 'mode'
    
    def on_quit(self):
        """Quit button clicked"""
        self.audio.play('click')
        self.action = 'quit'
    
    def handle_event(self, event):
        """Handle input events"""
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False
    
    def update(self, dt):
        """Update menu animations"""
        # Update ghost snakes
        for ghost in self.ghost_snakes:
            ghost.update(dt)
        
        # Update gradient animation
        self.gradient_offset = (self.gradient_offset + dt * 20) % 360
    
    def draw(self, surface):
        """Draw menu"""
        # Animated gradient background
        self._draw_animated_background(surface)
        
        # Draw ghost snakes
        for ghost in self.ghost_snakes:
            ghost.draw(surface, self.cell_size, 0, 0, alpha=80)
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill(self.theme['background'])
        surface.blit(overlay, (0, 0))
        
        # Draw title
        title_text = self.title_font.render("SNAKE AI", True, self.theme['snake_head'])
        title_shadow = self.title_font.render("SNAKE AI", True, self.theme['text_shadow'])
        title_rect = title_text.get_rect(center=(self.width // 2, 150))
        shadow_rect = title_shadow.get_rect(center=(self.width // 2 + 4, 154))
        
        surface.blit(title_shadow, shadow_rect)
        surface.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.subtitle_font.render(
            "Advanced AI Search Algorithms", True, self.theme['text']
        )
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 220))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
    
    def _draw_animated_background(self, surface):
        """Draw animated gradient background"""
        for y in range(self.height):
            # Calculate color based on y position and animation offset
            factor = (y / self.height + self.gradient_offset / 360) % 1.0
            
            # Interpolate between gradient colors
            color = self._interpolate_color(
                self.theme['background_gradient_start'],
                self.theme['background_gradient_end'],
                factor
            )
            
            pygame.draw.line(surface, color, (0, y), (self.width, y))
    
    def _interpolate_color(self, color1, color2, factor):
        """Interpolate between two colors"""
        return tuple(
            int(color1[i] + (color2[i] - color1[i]) * factor)
            for i in range(3)
        )
    
    def get_action(self):
        """Get menu action and reset"""
        action = self.action
        self.action = None
        return action
    
    def update_theme(self, theme_name):
        """Update menu theme"""
        self.theme = get_theme(theme_name)
        for button in self.buttons:
            button.update_theme(self.theme)


class SettingsMenu:
    """Settings menu screen"""
    
    def __init__(self, width, height, config, audio_manager):
        """Initialize settings menu"""
        self.width = width
        self.height = height
        self.config = config
        self.audio = audio_manager
        
        theme_name = config.get('visual', 'default_theme')
        self.theme = get_theme(theme_name)
        
        # Title
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 32)
        
        # Controls
        y_offset = 150
        x_center = width // 2
        
        # Volume slider
        self.volume_slider = Slider(
            x_center - 200, y_offset,
            400, 0, 100,
            config.get('audio', 'volume'),
            self.theme, label="Volume"
        )
        y_offset += 100
        
        # Speed slider
        self.speed_slider = Slider(
            x_center - 200, y_offset,
            400,
            config.get('game', 'min_fps'),
            config.get('game', 'max_fps'),
            config.get('game', 'default_fps'),
            self.theme, label="Game Speed (FPS)"
        )
        y_offset += 100
        
        # Sound toggle
        self.sound_toggle = Toggle(
            x_center - 30, y_offset,
            self.theme, label="Sound Effects",
            initial_state=config.get('audio', 'enabled')
        )
        y_offset += 100
        
        # Visualization toggle
        self.viz_toggle = Toggle(
            x_center - 30, y_offset,
            self.theme, label="Show AI Visualization",
            initial_state=config.get('ai', 'show_visualization')
        )
        y_offset += 100
        
        # Theme buttons
        self.theme_label_y = y_offset - 30
        button_y = y_offset + 10
        button_width = 120
        button_spacing = 140
        start_x = x_center - (button_spacing * 2)
        
        from snake_game.themes import get_theme_names
        theme_names = get_theme_names()
        
        self.theme_buttons = []
        for i, theme_name in enumerate(theme_names):
            btn = Button(
                start_x + i * button_spacing, button_y,
                button_width, 50,
                theme_name.upper(), self.theme,
                on_click=lambda t=theme_name: self.on_theme_change(t)
            )
            self.theme_buttons.append(btn)
        
        # Back button
        self.back_button = Button(
            x_center - 100, height - 120,
            200, 60,
            "BACK", self.theme, on_click=self.on_back
        )
        
        self.action = None
    
    def on_theme_change(self, theme_name):
        """Theme button clicked"""
        self.audio.play('click')
        self.config.set('visual', 'default_theme', value=theme_name)
        self.theme = get_theme(theme_name)
        self.update_all_themes()
    
    def update_all_themes(self):
        """Update theme for all UI components"""
        self.volume_slider.update_theme(self.theme)
        self.speed_slider.update_theme(self.theme)
        self.sound_toggle.update_theme(self.theme)
        self.viz_toggle.update_theme(self.theme)
        self.back_button.update_theme(self.theme)
        for btn in self.theme_buttons:
            btn.update_theme(self.theme)
    
    def on_back(self):
        """Back button clicked"""
        self.audio.play('click')
        # Save settings
        self.config.set('audio', 'volume', value=self.volume_slider.get_value())
        self.config.set('game', 'default_fps', value=self.speed_slider.get_value())
        self.config.set('audio', 'enabled', value=self.sound_toggle.get_state())
        self.config.set('ai', 'show_visualization', value=self.viz_toggle.get_state())
        self.config.save()
        
        # Update audio volume
        self.audio.set_volume(self.volume_slider.get_value())
        self.audio.enabled = self.sound_toggle.get_state()
        
        self.action = 'back'
    
    def handle_event(self, event):
        """Handle input events"""
        self.volume_slider.handle_event(event)
        self.speed_slider.handle_event(event)
        self.sound_toggle.handle_event(event)
        self.viz_toggle.handle_event(event)
        self.back_button.handle_event(event)
        
        for btn in self.theme_buttons:
            btn.handle_event(event)
        
        return False
    
    def update(self, dt):
        """Update settings menu"""
        pass
    
    def draw(self, surface):
        """Draw settings menu"""
        surface.fill(self.theme['background'])
        
        # Title
        title_text = self.title_font.render("SETTINGS", True, self.theme['text'])
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        surface.blit(title_text, title_rect)
        
        # Draw controls
        self.volume_slider.draw(surface)
        self.speed_slider.draw(surface)
        self.sound_toggle.draw(surface)
        self.viz_toggle.draw(surface)
        
        # Theme label
        theme_label = self.font.render("Theme:", True, self.theme['text'])
        surface.blit(theme_label, (self.width // 2 - 200, self.theme_label_y))
        
        # Theme buttons
        for btn in self.theme_buttons:
            btn.draw(surface)
        
        # Back button
        self.back_button.draw(surface)
    
    def get_action(self):
        """Get action and reset"""
        action = self.action
        self.action = None
        return action


class ModeMenu:
    """Mode selection menu"""
    
    def __init__(self, width, height, config, audio_manager):
        """Initialize mode menu"""
        self.width = width
        self.height = height
        self.config = config
        self.audio = audio_manager
        
        theme_name = config.get('visual', 'default_theme')
        self.theme = get_theme(theme_name)
        
        self.title_font = pygame.font.Font(None, 72)
        self.desc_font = pygame.font.Font(None, 24)
        
        # Mode buttons
        modes = [
            ('human', 'HUMAN', 'Play manually with arrow keys'),
            ('astar', 'A* SEARCH', 'Heuristic-guided optimal pathfinding'),
            ('bfs', 'BFS', 'Breadth-first shortest path search'),
            ('alphabeta', 'ALPHA-BETA', 'Minimax with adversarial search')
        ]
        
        button_width = 250
        button_height = 80
        spacing = 120
        start_y = 180
        x_left = width // 2 - button_width - 20
        x_right = width // 2 + 20
        
        self.mode_buttons = []
        self.mode_descriptions = {}
        
        for i, (mode_id, mode_name, desc) in enumerate(modes):
            x = x_left if i % 2 == 0 else x_right
            y = start_y + (i // 2) * spacing
            
            btn = Button(
                x, y, button_width, button_height,
                mode_name, self.theme,
                on_click=lambda m=mode_id: self.on_mode_select(m)
            )
            self.mode_buttons.append(btn)
            self.mode_descriptions[mode_id] = desc
        
        # Back button
        self.back_button = Button(
            width // 2 - 100, height - 120,
            200, 60,
            "BACK", self.theme, on_click=self.on_back
        )
        
        self.selected_mode = config.get('ai', 'default_mode')
        self.action = None
    
    def on_mode_select(self, mode):
        """Mode button clicked"""
        self.audio.play('click')
        self.selected_mode = mode
        self.config.set('ai', 'default_mode', value=mode)
        self.config.save()
    
    def on_back(self):
        """Back button clicked"""
        self.audio.play('click')
        self.action = 'back'
    
    def handle_event(self, event):
        """Handle input events"""
        for btn in self.mode_buttons:
            btn.handle_event(event)
        self.back_button.handle_event(event)
        return False
    
    def update(self, dt):
        """Update mode menu"""
        pass
    
    def draw(self, surface):
        """Draw mode menu"""
        surface.fill(self.theme['background'])
        
        # Title
        title_text = self.title_font.render("SELECT MODE", True, self.theme['text'])
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        surface.blit(title_text, title_rect)
        
        # Current mode indicator
        current_text = self.desc_font.render(
            f"Current: {self.selected_mode.upper()}", 
            True, self.theme['snake_head']
        )
        current_rect = current_text.get_rect(center=(self.width // 2, 130))
        surface.blit(current_text, current_rect)
        
        # Draw mode buttons
        for btn in self.mode_buttons:
            btn.draw(surface)
        
        # Back button
        self.back_button.draw(surface)
    
    def get_action(self):
        """Get action and reset"""
        action = self.action
        self.action = None
        return action
    
    def update_theme(self, theme_name):
        """Update theme"""
        self.theme = get_theme(theme_name)
        for btn in self.mode_buttons:
            btn.update_theme(self.theme)
        self.back_button.update_theme(self.theme)