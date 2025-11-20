"""
Button component for UI
"""
import pygame


class Button:
    """Interactive button with hover and click states"""
    
    def __init__(self, x, y, width, height, text, theme, on_click=None):
        """
        Initialize button
        
        Args:
            x, y: Position
            width, height: Size
            text: Button text
            theme: Theme dictionary
            on_click: Callback function
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.theme = theme
        self.on_click = on_click
        self.hovered = False
        self.pressed = False
        self.font = pygame.font.Font(None, 36)
    
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                self.pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.hovered and event.button == 1:
                self.pressed = False
                if self.on_click:
                    self.on_click()
                return True
            self.pressed = False
        
        return False
    
    def draw(self, surface):
        """Draw button on surface"""
        # Determine color based on state
        if self.pressed:
            color = self.theme['button_active']
        elif self.hovered:
            color = self.theme['button_hover']
        else:
            color = self.theme['button_bg']
        
        # Draw button background with rounded corners
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        # Draw border
        border_color = self.theme['button_text']
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=10)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.theme['button_text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def update_theme(self, theme):
        """Update button theme"""
        self.theme = theme


class Slider:
    """Slider component for numeric values"""
    
    def __init__(self, x, y, width, min_val, max_val, initial_val, theme, label=""):
        """
        Initialize slider
        
        Args:
            x, y: Position
            width: Slider width
            min_val: Minimum value
            max_val: Maximum value
            initial_val: Initial value
            theme: Theme dictionary
            label: Label text
        """
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.theme = theme
        self.label = label
        self.dragging = False
        
        self.track_rect = pygame.Rect(x, y, width, 10)
        self.handle_radius = 12
        self.font = pygame.font.Font(None, 28)
    
    def handle_event(self, event):
        """Handle mouse events"""
        handle_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        handle_pos = (handle_x, self.y + 5)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dist = ((event.pos[0] - handle_pos[0])**2 + (event.pos[1] - handle_pos[1])**2)**0.5
                if dist <= self.handle_radius:
                    self.dragging = True
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Update value based on mouse position
                relative_x = max(0, min(self.width, event.pos[0] - self.x))
                self.value = self.min_val + (relative_x / self.width) * (self.max_val - self.min_val)
                self.value = int(self.value)
                return True
        
        return False
    
    def draw(self, surface):
        """Draw slider on surface"""
        # Draw label
        if self.label:
            label_surface = self.font.render(f"{self.label}: {self.value}", True, self.theme['text'])
            surface.blit(label_surface, (self.x, self.y - 30))
        
        # Draw track
        pygame.draw.rect(surface, self.theme['grid'], self.track_rect, border_radius=5)
        
        # Draw filled portion
        filled_width = (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        filled_rect = pygame.Rect(self.x, self.y, filled_width, 10)
        pygame.draw.rect(surface, self.theme['path'], filled_rect, border_radius=5)
        
        # Draw handle
        handle_x = self.x + filled_width
        handle_pos = (int(handle_x), self.y + 5)
        pygame.draw.circle(surface, self.theme['button_hover'], handle_pos, self.handle_radius)
        pygame.draw.circle(surface, self.theme['text'], handle_pos, self.handle_radius, 2)
    
    def get_value(self):
        """Get current value"""
        return int(self.value)
    
    def set_value(self, value):
        """Set slider value"""
        self.value = max(self.min_val, min(self.max_val, value))
    
    def update_theme(self, theme):
        """Update slider theme"""
        self.theme = theme


class Toggle:
    """Toggle switch component"""
    
    def __init__(self, x, y, theme, label="", initial_state=True):
        """
        Initialize toggle
        
        Args:
            x, y: Position
            theme: Theme dictionary
            label: Label text
            initial_state: Initial on/off state
        """
        self.x = x
        self.y = y
        self.theme = theme
        self.label = label
        self.state = initial_state
        
        self.width = 60
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.font = pygame.font.Font(None, 28)
    
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.state = not self.state
                return True
        return False
    
    def draw(self, surface):
        """Draw toggle on surface"""
        # Draw label
        if self.label:
            label_surface = self.font.render(self.label, True, self.theme['text'])
            surface.blit(label_surface, (self.x, self.y - 30))
        
        # Draw track
        track_color = self.theme['snake_head'] if self.state else self.theme['grid']
        pygame.draw.rect(surface, track_color, self.rect, border_radius=15)
        
        # Draw handle
        handle_x = self.x + self.width - 15 if self.state else self.x + 15
        handle_pos = (handle_x, self.y + 15)
        pygame.draw.circle(surface, self.theme['button_text'], handle_pos, 12)
    
    def get_state(self):
        """Get toggle state"""
        return self.state
    
    def set_state(self, state):
        """Set toggle state"""
        self.state = state
    
    def update_theme(self, theme):
        """Update toggle theme"""
        self.theme = theme