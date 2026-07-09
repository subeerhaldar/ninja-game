import pygame

class Button:
    def __init__(self, x, y, width, height, text, bg_color, text_color=(255, 255, 255), font_size=36, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)
        self.callback = callback
        
        # Hover effect handling
        self.is_hovered = False
        
    def draw(self, surface):
        # Slightly lighten color if hovered
        color = self.bg_color
        if self.is_hovered:
            # Simple highlight logic: clamp values to 255
            color = tuple(min(255, c + 30) for c in self.bg_color)
            
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        
        # Render text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered: # Left click
                if self.callback:
                    self.callback()

class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        
    def take_damage(self, amount):
        self.current_health = max(0, self.current_health - amount)
        
    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)
        
    def draw(self, surface):
        # Background (empty health)
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, (100, 100, 100), bg_rect, border_radius=4)
        
        # Foreground (current health)
        health_ratio = self.current_health / self.max_health
        health_width = int(self.width * health_ratio)
        
        if health_width > 0:
            # Color dynamically shifts from red to green based on health
            r = min(255, int(255 * (1 - health_ratio) * 2))
            g = min(255, int(255 * health_ratio * 2))
            color = (r, g, 0)
            
            fg_rect = pygame.Rect(self.x, self.y, health_width, self.height)
            pygame.draw.rect(surface, color, fg_rect, border_radius=4)
            
        # Draw outline
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, width=2, border_radius=4)

