import pygame

ELEMENT_COLORS = {
    "Darkness": (150, 100, 255),  # Purple
    "Fire": (255, 100, 100),      # Red
    "Ice": (150, 230, 255),       # Light Blue
    "Wind": (150, 255, 150),      # Light Green
    "Earth": (200, 150, 100),     # Brown
    "Water": (100, 150, 255),     # Blue
    "Lightning": (255, 255, 100), # Yellow
    "Poison": (200, 100, 255),    # Magenta
    "Light": (255, 255, 200),     # Bright Yellow
    "Metal": (200, 200, 200),     # Gray
    "Blood": (255, 50, 50),       # Dark Red
    "Wood": (100, 200, 100),      # Forest Green
    "Sand": (255, 200, 150),      # Sand
}

class Ninja(pygame.sprite.Sprite):
    def __init__(self, x, y, element=None):
        super().__init__()
        # Load realistic sprite if available
        # Load realistic sprite if available
        try:
            raw_image = pygame.image.load("assets/ninja.png").convert_alpha()
            self.original_image = pygame.transform.scale(raw_image, (60, 80))
            
            # Apply element tint
            if element and element in ELEMENT_COLORS:
                tint = ELEMENT_COLORS[element]
                # Multiply color
                color_surf = pygame.Surface(self.original_image.get_size()).convert_alpha()
                color_surf.fill((*tint, 255))
                self.original_image.blit(color_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
            self.flipped_image = pygame.transform.flip(self.original_image, True, False)
            self.image = self.original_image
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill((0, 0, 255)) # Blue character
            self.original_image = self.image
            self.flipped_image = self.image
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing_right = True
        
        # Movement physics
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.5
        
        # State
        self.on_ground = False
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.facing_right = True
        else:
            self.velocity.x = 0
            
        # Jump (Only allow jumping if on the ground)
        # Using UP arrow for jumping so SPACE can still be used for MENU transitions
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_power
            self.on_ground = False

    def apply_gravity(self):
        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y
        
    def update(self, platforms):
        self.get_input()
        
        # Update sprite facing direction
        if self.facing_right:
            self.image = self.original_image
        else:
            self.image = self.flipped_image
        
        # 1. Update X position
        self.rect.x += self.velocity.x
        
        # Handle X collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0: # Moving right
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0: # Moving left
                    self.rect.left = platform.rect.right
                    
        # 2. Update Y position and apply gravity
        self.apply_gravity()
        
        # Handle Y collisions
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0: # Falling
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0: # Jumping and hit head
                    self.velocity.y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        try:
            raw_plat = pygame.image.load("assets/platform.png").convert_alpha()
            self.image = pygame.transform.scale(raw_plat, (width, height))
        except:
            self.image = pygame.Surface((width, height))
            self.image.fill((0, 255, 0)) # Green platform
        self.rect = self.image.get_rect(topleft=(x, y))

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 0)) # Yellow goal
        self.rect = self.image.get_rect(topleft=(x, y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0)) # Red spikes/lava
        self.rect = self.image.get_rect(topleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            raw_image = pygame.image.load("assets/ninja.png").convert_alpha()
            self.original_image = pygame.transform.scale(raw_image, (60, 80))
            # Tint black for evil clone look
            color_surf = pygame.Surface(self.original_image.get_size()).convert_alpha()
            color_surf.fill((50, 50, 50, 255))
            self.original_image.blit(color_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.flipped_image = pygame.transform.flip(self.original_image, True, False)
            self.image = self.original_image
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill((100, 0, 100)) # Purple block fallback
            self.original_image = self.image
            self.flipped_image = self.image
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing_right = True
        self.speed = 2
        self.velocity_y = 0
        self.gravity = 0.5
        
    def update(self, platforms):
        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # Handle Y collisions
        on_ground = False
        current_platform = None
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0: # Falling
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    on_ground = True
                    current_platform = platform
                    
        # Patrol logic (turn around at edges)
        if on_ground and current_platform:
            if self.facing_right:
                self.rect.x += self.speed
                self.image = self.original_image
                if self.rect.right > current_platform.rect.right:
                    self.facing_right = False
                    self.rect.right = current_platform.rect.right
            else:
                self.rect.x -= self.speed
                self.image = self.flipped_image
                if self.rect.left < current_platform.rect.left:
                    self.facing_right = True
                    self.rect.left = current_platform.rect.left
