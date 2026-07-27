import pygame
from settings import *
from timer import Timer


class TeleporterMenu:
    """Simple teleporter UI: shows available teleport locations."""
    def __init__(self, player, close_menu_callback):
        """Set up teleport locations."""
        self.player = player
        self.close_menu_callback = close_menu_callback
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font("font/LycheeSoda.ttf", 30)
        
        # Define teleport locations (add more as needed)
        self.locations = {
            "Trader": (1400, 1200),      # Trader location
            "Beach": (2000, 1800),       # Shore/ocean location (adjust to your map)
            "Home": (200, 300),          # Player's home
        }
        
        self.options = list(self.locations.keys())
        self.index = 0
        self.timer = Timer(200)
        self.setup()
    
    def setup(self):
        """Pre-render text and calculate menu size."""
        self.text_surfs = []
        self.total_height = 0
        padding = 8
        space = 10
        
        for location in self.options:
            text_surf = self.font.render(location, False, "Black")
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (padding * 2)
        
        self.total_height += (len(self.text_surfs) - 1) * space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.width = 300
        self.main_rect = pygame.Rect(
            SCREEN_WIDTH / 2 - self.width / 2,
            self.menu_top,
            self.width,
            self.total_height,
        )
    
    def input(self):
        """Handle navigation and teleportation."""
        keys = pygame.key.get_pressed()
        self.timer.update()
        
        if keys[pygame.K_ESCAPE]:
            self.close_menu_callback()
            return
        
        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()
            
            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()
            
            if keys[pygame.K_SPACE]:
                # Teleport to selected location
                location_name = self.options[self.index]
                target_pos = self.locations[location_name]
                self.player.rect.center = target_pos
                self.player.pos = pygame.math.Vector2(target_pos)
                self.close_menu_callback()
                self.timer.activate()
        
        # Clamp index
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index >= len(self.options):
            self.index = 0
    
    def display(self):
        """Draw the teleporter menu."""
        padding = 8
        space = 10
        
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (
                text_surf.get_height() + (padding * 2) + space
            )
            
            # Background
            bg_rect = pygame.Rect(
                self.main_rect.left,
                top,
                self.width,
                text_surf.get_height() + (padding * 2),
            )
            pygame.draw.rect(self.display_surface, "White", bg_rect, 0, 4)
            
            # Text
            text_rect = text_surf.get_rect(
                midleft=(self.main_rect.left + 20, bg_rect.centery)
            )
            self.display_surface.blit(text_surf, text_rect)
            
            # Highlight selected
            if self.index == text_index:
                pygame.draw.rect(self.display_surface, "Black", bg_rect, 4, 4)
    
    def update(self):
        """Process input each frame."""
        self.input()