"""
Theme definitions for Snake AI Game
Each theme defines colors for all visual elements
"""

THEMES = {
    'neon': {
        'name': 'Neon',
        'background': (10, 10, 25),
        'background_gradient_start': (10, 10, 25),
        'background_gradient_end': (20, 5, 40),
        'grid': (30, 30, 60),
        'snake_head': (0, 255, 150),
        'snake_body_start': (0, 255, 150),
        'snake_body_end': (0, 150, 255),
        'snake_eye': (255, 255, 255),
        'snake_pupil': (0, 0, 0),
        'food': (255, 0, 100),
        'food_glow': (255, 50, 150),
        'text': (255, 255, 255),
        'text_shadow': (100, 0, 255),
        'visited': (40, 40, 80),
        'frontier': (60, 60, 120),
        'path': (255, 255, 0),
        'path_glow': (255, 200, 0),
        'button_bg': (50, 50, 100),
        'button_hover': (80, 80, 150),
        'button_active': (100, 100, 200),
        'button_text': (255, 255, 255),
        'menu_overlay': (10, 10, 25, 200),
    },
    
    'pastel': {
        'name': 'Pastel',
        'background': (250, 240, 245),
        'background_gradient_start': (250, 240, 245),
        'background_gradient_end': (240, 230, 255),
        'grid': (220, 210, 225),
        'snake_head': (150, 200, 150),
        'snake_body_start': (150, 200, 150),
        'snake_body_end': (100, 180, 220),
        'snake_eye': (255, 255, 255),
        'snake_pupil': (50, 50, 50),
        'food': (255, 150, 150),
        'food_glow': (255, 180, 180),
        'text': (80, 80, 100),
        'text_shadow': (200, 200, 220),
        'visited': (235, 225, 240),
        'frontier': (225, 215, 235),
        'path': (255, 200, 100),
        'path_glow': (255, 220, 150),
        'button_bg': (200, 190, 210),
        'button_hover': (180, 170, 200),
        'button_active': (160, 150, 190),
        'button_text': (80, 80, 100),
        'menu_overlay': (250, 240, 245, 220),
    },
    
    'dark': {
        'name': 'Dark',
        'background': (18, 18, 18),
        'background_gradient_start': (18, 18, 18),
        'background_gradient_end': (25, 25, 30),
        'grid': (40, 40, 40),
        'snake_head': (76, 175, 80),
        'snake_body_start': (76, 175, 80),
        'snake_body_end': (56, 142, 60),
        'snake_eye': (255, 255, 255),
        'snake_pupil': (0, 0, 0),
        'food': (244, 67, 54),
        'food_glow': (255, 100, 90),
        'text': (255, 255, 255),
        'text_shadow': (100, 100, 100),
        'visited': (33, 33, 33),
        'frontier': (50, 50, 50),
        'path': (255, 235, 59),
        'path_glow': (255, 245, 100),
        'button_bg': (50, 50, 50),
        'button_hover': (70, 70, 70),
        'button_active': (90, 90, 90),
        'button_text': (255, 255, 255),
        'menu_overlay': (18, 18, 18, 200),
    },
    
    'classic': {
        'name': 'Classic',
        'background': (170, 215, 81),
        'background_gradient_start': (170, 215, 81),
        'background_gradient_end': (162, 209, 73),
        'grid': (162, 209, 73),
        'snake_head': (43, 51, 24),
        'snake_body_start': (43, 51, 24),
        'snake_body_end': (60, 70, 35),
        'snake_eye': (255, 255, 200),
        'snake_pupil': (0, 0, 0),
        'food': (180, 34, 34),
        'food_glow': (200, 50, 50),
        'text': (43, 51, 24),
        'text_shadow': (200, 220, 150),
        'visited': (180, 220, 90),
        'frontier': (175, 215, 85),
        'path': (255, 200, 50),
        'path_glow': (255, 220, 100),
        'button_bg': (140, 180, 60),
        'button_hover': (120, 160, 50),
        'button_active': (100, 140, 40),
        'button_text': (43, 51, 24),
        'menu_overlay': (170, 215, 81, 220),
    }
}


def get_theme(theme_name):
    """
    Get theme by name with fallback to neon
    
    Args:
        theme_name: Name of the theme
        
    Returns:
        Theme dictionary
    """
    return THEMES.get(theme_name.lower(), THEMES['neon'])


def get_theme_names():
    """Get list of available theme names"""
    return list(THEMES.keys())


def interpolate_color(color1, color2, factor):
    """
    Interpolate between two colors
    
    Args:
        color1: RGB tuple
        color2: RGB tuple
        factor: 0.0 to 1.0
        
    Returns:
        Interpolated RGB tuple
    """
    return tuple(
        int(color1[i] + (color2[i] - color1[i]) * factor)
        for i in range(3)
    )