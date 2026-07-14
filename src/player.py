import pygame

ELEMENT_COLORS = {
    "Darkness": (120, 80, 220),   # Purple/Indigo
    "Fire": (255, 69, 0),         # OrangeRed
    "Ice": (175, 238, 238),        # PaleTurquoise
    "Wind": (152, 251, 152),       # PaleGreen
    "Earth": (139, 69, 19),        # SaddleBrown
    "Water": (30, 144, 255),       # DodgerBlue
    "Lightning": (255, 215, 0),    # Gold
    "Poison": (148, 0, 211),       # DarkViolet
    "Light": (255, 250, 205),      # LemonChiffon
    "Metal": (192, 192, 192),      # Silver
    "Spirit": (224, 255, 255),     # LightCyan
    "Blood": (178, 34, 34),        # Firebrick
    "Wood": (34, 139, 34),         # ForestGreen
    "Beast": (205, 133, 63),       # Peru
    "Sand": (244, 164, 96),        # SandyBrown
    "Lunar": (230, 230, 250),      # Lavender
    "Solar": (255, 140, 0),        # DarkOrange
    "Gravity": (106, 90, 205),     # SlateBlue
    "Time": (70, 130, 180),        # SteelBlue
    "Void": (25, 25, 112),         # MidnightBlue
    "Sound": (218, 112, 214),      # Orchid
    "Crystal": (240, 248, 255),    # AliceBlue
    "Magma": (255, 99, 71),        # Tomato
    "Storm": (119, 136, 153),      # LightSlateGray
    "Illusion": (255, 105, 180),   # HotPink
    "Bone": (245, 245, 220),       # Beige
    "Death": (47, 79, 79),         # DarkSlateGray
    "Psychic": (255, 0, 255),      # Fuchsia
    "Plasma": (0, 255, 255),       # Cyan
    "Mirror": (240, 255, 240),     # Honeydew
    "Smoke": (105, 105, 105),      # DimGray
    "Ash": (128, 128, 128),        # Gray
}

class Ninja(pygame.sprite.Sprite):
    def __init__(self, x, y, character, env_color=None):
        super().__init__()
        self.character = character
        self.duo = character # For backwards compatibility with main.py references
        self.env_color = env_color
        
        # Extract properties
        if hasattr(character, 'element'):
            self.element = character.element
            self.name = character.name
            self.sprite_file = character.sprite_file
        else:
            self.element = character if isinstance(character, str) else None
            self.name = "Ninja"
            self.sprite_file = "player_naruto.png"
            
        # Load character-specific images
        self.original_image, self.flipped_image = self.load_character_images()
        self.image = self.original_image
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing_right = True
        
        # Movement physics
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.jump_power = -12.5
        self.gravity = 0.5
        self.on_ground = False
        
    def load_character_images(self):
        # Try loading custom character sprite
        try:
            raw_image = pygame.image.load(f"assets/{self.sprite_file}").convert()
            raw_image.set_colorkey((0, 0, 0))
            raw_image = raw_image.convert_alpha()
            img = pygame.transform.scale(raw_image, (60, 80))
            flipped_img = pygame.transform.flip(img, True, False)
            return img, flipped_img
        except:
            # Fallback to player_naruto.png tinted with element color
            try:
                raw_image = pygame.image.load("assets/player_naruto.png").convert()
                raw_image.set_colorkey((0, 0, 0))
                raw_image = raw_image.convert_alpha()
                img = pygame.transform.scale(raw_image, (60, 80))
                
                tint = ELEMENT_COLORS.get(self.element, (255, 255, 255))
                color_surf = pygame.Surface(img.get_size()).convert_alpha()
                color_surf.fill((*tint, 255))
                img.blit(color_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                flipped_img = pygame.transform.flip(img, True, False)
                return img, flipped_img
            except:
                # Absolute fallback
                img = pygame.Surface((40, 60))
                color = ELEMENT_COLORS.get(self.element, (0, 0, 255))
                img.fill(color)
                return img, img
                
    def switch_ninja(self):
        # Swapping is disabled now, but key is bound to a visual chakra burst in main.py
        pass
        
    def get_active_name(self):
        return self.name

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
    def __init__(self, x, y, width, height, element_color=None):
        super().__init__()
        try:
            raw_plat = pygame.image.load("assets/platform.png").convert_alpha()
            self.image = pygame.transform.scale(raw_plat, (width, height))
            if element_color:
                color_surf = pygame.Surface(self.image.get_size()).convert_alpha()
                # Standard blend with alpha to preserve texture details and keep it bright
                color_surf.fill((*element_color, 90))
                self.image.blit(color_surf, (0, 0))
                
            # Define high-contrast bright border
            border_color = (255, 255, 255)
            if element_color:
                max_val = max(element_color)
                if max_val > 0:
                    border_color = tuple(min(255, int(c * 255 / max_val)) for c in element_color)
                    # Boost brightness if it is too dark
                    if sum(border_color) < 250:
                        border_color = (255, 220, 100) # Bright gold/yellow
                        
            # Draw top highlight line (3px thick)
            pygame.draw.line(self.image, border_color, (0, 1), (width, 1), 3)
            # Draw 1px rectangle outline around the platform
            pygame.draw.rect(self.image, border_color, (0, 0, width, height), 1)
        except:
            self.image = pygame.Surface((width, height))
            color = element_color if element_color else (0, 255, 0)
            self.image.fill(color)
            pygame.draw.rect(self.image, (255, 255, 255), (0, 0, width, height), 2)
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
            raw_image = pygame.image.load("assets/ninja.png").convert()
            raw_image.set_colorkey((0, 0, 0))
            raw_image = raw_image.convert_alpha()
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
