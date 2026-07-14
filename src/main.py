import pygame
import sys
import random
import io
import struct
import math
from game_state import GameState
from roster import ROSTER
from ui import Button
from player import Ninja, Platform, Goal, Obstacle, Enemy, ELEMENT_COLORS
from levels import LEVELS

# Window settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Basic Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ninja Game")
    clock = pygame.time.Clock()
    
    state_data = {
        "current_state": GameState.MENU,
        "selected_index": 0,
        "current_level": 0,
        "won": False
    }
    
    # A default font for rendering text placeholders
    font = pygame.font.SysFont(None, 48)
    title_font = pygame.font.SysFont(None, 64)
    desc_font = pygame.font.SysFont(None, 32)
    
    # Load realistic background
    try:
        base_bg_image = pygame.image.load("assets/bg.png").convert()
        base_bg_image = pygame.transform.scale(base_bg_image, (WIDTH, HEIGHT))
    except:
        base_bg_image = None
        
    bg_image = base_bg_image

    # Chiptune generator supporting multiple wave types for random chiptune sounds
    def make_chiptune_track(notes, tempo=120, sample_rate=22050):
        beat_duration = 60.0 / tempo
        samples = bytearray()
        for freq, beats in notes:
            duration = beats * beat_duration
            num_samples = int(duration * sample_rate)
            
            # Select random retro wave type for each note to make a variety of sounds
            wave_type = random.choice(["square", "triangle", "noise"])
            
            for i in range(num_samples):
                if freq == 0:
                    val_int = 0
                else:
                    period = sample_rate / freq
                    decay = 1.0 - (i / num_samples)
                    volume = 0.08 * decay # soft background sound volume
                    
                    if wave_type == "square":
                        is_high = (i % period) < (period / 2)
                        val = volume if is_high else -volume
                    elif wave_type == "triangle":
                        t = (i % period) / period
                        val = volume * (4 * t - 1) if t < 0.5 else volume * (3 - 4 * t)
                    else: # noise
                        val = random.uniform(-volume, volume)
                        
                    val_int = int(val * 32767)
                    
                samples.extend(struct.pack('<h', val_int))
                
        # 44 bytes WAV header
        num_channels = 1
        bytes_per_sample = 2
        byte_rate = sample_rate * num_channels * bytes_per_sample
        block_align = num_channels * bytes_per_sample
        data_size = len(samples)
        chunk_size = 36 + data_size
        
        header = struct.pack(
            '<4sI4s4sIHHIIHH4sI',
            b'RIFF', chunk_size, b'WAVE', b'fmt ', 16, 1,
            num_channels, sample_rate, byte_rate, block_align,
            16, b'data', data_size
        )
        return pygame.mixer.Sound(file=io.BytesIO(header + samples))

    current_music_channel = None
    current_music_sound = None

    def play_environment_music(level_index):
        nonlocal current_music_channel, current_music_sound
        
        if current_music_channel:
            try:
                current_music_channel.stop()
            except:
                pass
                
        env_name, _ = get_env_for_level(level_index)
        
        # Build a randomized set of chiptune notes and sounds!
        # C major pentatonic, minor, and exotic frequency scales
        if env_name == "Forest":
            freqs = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25]
            tempo = random.randint(120, 150)
        elif env_name == "Volcano":
            freqs = [220.00, 233.08, 261.63, 277.18, 311.13, 329.63]
            tempo = random.randint(160, 190)
        elif env_name == "Glacier":
            freqs = [587.33, 659.25, 783.99, 880.00, 987.77, 1046.50]
            tempo = random.randint(80, 110)
        elif env_name == "Desert":
            freqs = [293.66, 311.13, 369.99, 392.00, 440.00, 466.16]
            tempo = random.randint(110, 130)
        else: # Void
            freqs = [110.00, 130.81, 146.83, 164.81, 220.00, 261.63]
            tempo = random.randint(70, 90)
            
        # Build sequence of 20 random notes/sound effects!
        notes = []
        for _ in range(20):
            if random.random() < 0.8:
                freq = random.choice(freqs)
            else:
                freq = 0 # rest / pause
            # Random duration (beats)
            beats = random.choice([0.25, 0.5, 0.75, 1.0])
            notes.append((freq, beats))
            
        try:
            current_music_sound = make_chiptune_track(notes, tempo)
            current_music_channel = current_music_sound.play(loops=-1)
        except Exception as e:
            print("Audio error:", e)

    def stop_music():
        nonlocal current_music_channel
        if current_music_channel:
            try:
                current_music_channel.stop()
            except:
                pass

    # Level environment definitions: (Name, color)
    LEVEL_ENVIRONMENTS = [
        ("Forest", (50, 180, 50)),      # Levels 1-3
        ("Volcano", (220, 70, 30)),     # Levels 4-6
        ("Glacier", (130, 220, 255)),   # Levels 7-9
        ("Desert", (230, 180, 80)),     # Levels 10-12
        ("Void", (120, 50, 200))        # Levels 13-15
    ]

    def get_env_for_level(level_index):
        if level_index < 3:
            return LEVEL_ENVIRONMENTS[0]
        elif level_index < 6:
            return LEVEL_ENVIRONMENTS[1]
        elif level_index < 9:
            return LEVEL_ENVIRONMENTS[2]
        elif level_index < 12:
            return LEVEL_ENVIRONMENTS[3]
        else:
            return LEVEL_ENVIRONMENTS[4]

    def create_tinted_bg(env_color, element_color):
        if base_bg_image is None:
            return None
        tinted = base_bg_image.copy()
        r = int(env_color[0] * 0.6 + element_color[0] * 0.4)
        g = int(env_color[1] * 0.6 + element_color[1] * 0.4)
        b = int(env_color[2] * 0.6 + element_color[2] * 0.4)
        
        overlay = pygame.Surface(tinted.get_size()).convert_alpha()
        overlay.fill((r, g, b, 80))
        tinted.blit(overlay, (0, 0))
        return tinted

    # Active dynamic background
    active_bg = None
    
    # Particles list
    particles = []
    
    class GameParticle:
        def __init__(self, x, y, vx, vy, color, size, lifetime, shape="circle"):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.color = color
            self.size = size
            self.lifetime = lifetime
            self.max_lifetime = lifetime
            self.shape = shape
            
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.lifetime -= 1
            
        def draw(self, surface):
            if self.lifetime <= 0:
                return
            try:
                if self.shape == "circle":
                    pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
                elif self.shape == "leaf":
                    rect = pygame.Rect(int(self.x - self.size), int(self.y - self.size/2), int(self.size * 2), int(self.size))
                    pygame.draw.ellipse(surface, self.color, rect)
                elif self.shape == "spark":
                    pygame.draw.line(surface, self.color, (int(self.x), int(self.y)), (int(self.x - self.vx * 2), int(self.y - self.vy * 2)), int(self.size))
                elif self.shape == "raindrop":
                    pygame.draw.line(surface, self.color, (int(self.x), int(self.y)), (int(self.x + self.vx), int(self.y + self.vy)), int(self.size))
                else:
                    rect = pygame.Rect(int(self.x - self.size/2), int(self.y - self.size/2), int(self.size), int(self.size))
                    pygame.draw.rect(surface, self.color, rect)
            except:
                pass

    def update_and_draw_particles(screen):
        for p in particles[:]:
            p.update()
            if p.lifetime <= 0:
                particles.remove(p)
            else:
                p.draw(screen)

    def spawn_level_particles(level_index, duo_element):
        env_name, env_color = get_env_for_level(level_index)
        elem_color = ELEMENT_COLORS.get(duo_element, (255, 255, 255))
        
        if duo_element in ["Fire", "Magma", "Solar", "Plasma"]:
            particles.append(GameParticle(
                random.randint(0, WIDTH), HEIGHT,
                random.uniform(-1, 1), random.uniform(-3, -1),
                elem_color, random.randint(3, 6), random.randint(60, 100), "circle"
            ))
        elif duo_element in ["Ice", "Crystal", "Lunar"]:
            particles.append(GameParticle(
                random.randint(0, WIDTH), 0,
                random.uniform(-1, 1), random.uniform(1, 3),
                elem_color, random.randint(2, 5), random.randint(120, 200), "circle"
            ))
        elif duo_element in ["Wind", "Wood", "Silent Owls"]:
            particles.append(GameParticle(
                random.randint(0, WIDTH), 0,
                random.uniform(-2, 2), random.uniform(1, 2.5),
                elem_color, random.randint(4, 7), random.randint(150, 250), "leaf"
            ))
        elif duo_element in ["Water", "Storm", "Aqua Dancers", "Sonic Booms"]:
            particles.append(GameParticle(
                random.randint(0, WIDTH), 0,
                3, random.uniform(8, 12),
                elem_color, random.randint(1, 2), random.randint(40, 70), "raindrop"
            ))
        elif duo_element in ["Lightning", "Psychic", "Spirit"]:
            if random.random() < 0.15:
                particles.append(GameParticle(
                    random.randint(0, WIDTH), random.randint(0, HEIGHT),
                    random.uniform(-2, 2), random.uniform(-2, 2),
                    elem_color, random.randint(2, 4), random.randint(15, 30), "spark"
                ))
        elif duo_element in ["Sand", "Earth", "Gravity"]:
            particles.append(GameParticle(
                0, random.randint(0, HEIGHT),
                random.uniform(2, 5), random.uniform(-0.5, 0.5),
                elem_color, random.randint(2, 4), random.randint(100, 180), "circle"
            ))
        elif duo_element in ["Darkness", "Poison", "Death", "Smoke", "Ash"]:
            particles.append(GameParticle(
                random.randint(0, WIDTH), HEIGHT,
                random.uniform(-0.5, 0.5), random.uniform(-2, -0.5),
                elem_color, random.randint(4, 8), random.randint(80, 120), "circle"
            ))
        else:
            if env_name == "Forest":
                particles.append(GameParticle(
                    random.randint(0, WIDTH), 0,
                    random.uniform(-1, 1), random.uniform(1, 2),
                    (100, 220, 100), random.randint(3, 6), random.randint(120, 200), "leaf"
                ))
            elif env_name == "Volcano":
                particles.append(GameParticle(
                    random.randint(0, WIDTH), HEIGHT,
                    random.uniform(-0.8, 0.8), random.uniform(-2.5, -1),
                    (255, 100, 0), random.randint(3, 5), random.randint(80, 130), "circle"
                ))
            elif env_name == "Glacier":
                particles.append(GameParticle(
                    random.randint(0, WIDTH), 0,
                    random.uniform(-0.5, 0.5), random.uniform(1, 2),
                    (200, 240, 255), random.randint(2, 4), random.randint(150, 220), "circle"
                ))
            else:
                if random.random() < 0.3:
                    particles.append(GameParticle(
                        random.randint(0, WIDTH), random.randint(0, HEIGHT),
                        random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5),
                        (200, 200, 200), random.randint(2, 3), random.randint(50, 100), "circle"
                    ))

    def spawn_switch_burst(pos, element):
        elem_color = ELEMENT_COLORS.get(element, (255, 255, 255))
        for _ in range(30):
            vx = random.uniform(-4, 4)
            vy = random.uniform(-4, 4)
            particles.append(GameParticle(
                pos[0], pos[1],
                vx, vy,
                elem_color, random.randint(3, 6), random.randint(20, 45), "spark"
            ))
    
    def on_prev():
        state_data["selected_index"] = (state_data["selected_index"] - 1) % len(ROSTER)
        
    def on_next():
        state_data["selected_index"] = (state_data["selected_index"] + 1) % len(ROSTER)
        
    def on_random():
        state_data["selected_index"] = random.randint(0, len(ROSTER) - 1)
        
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = None

    def load_level(level_index):
        nonlocal player, active_bg
        all_sprites.empty()
        platforms.empty()
        goals.empty()
        obstacles.empty()
        enemies.empty()
        particles.clear()
        
        level_data = LEVELS[level_index]
        duo = ROSTER[state_data["selected_index"]]
        
        env_name, env_color = get_env_for_level(level_index)
        elem_color = ELEMENT_COLORS.get(duo.element, (255, 255, 255))
        
        # Create tinted background
        active_bg = create_tinted_bg(env_color, elem_color)
        
        # Platform tint
        plat_tint = (
            int(env_color[0] * 0.4 + elem_color[0] * 0.6),
            int(env_color[1] * 0.4 + elem_color[1] * 0.6),
            int(env_color[2] * 0.4 + elem_color[2] * 0.6)
        )
        
        # Spawn platforms
        for p in level_data["platforms"]:
            plat = Platform(p[0], p[1], p[2], p[3], plat_tint)
            platforms.add(plat)
            all_sprites.add(plat)
            
        # Spawn obstacles
        for o in level_data.get("obstacles", []):
            obs = Obstacle(o[0], o[1], o[2], o[3])
            obstacles.add(obs)
            all_sprites.add(obs)
            
        # Spawn enemies
        for e in level_data.get("enemies", []):
            en = Enemy(e[0], e[1])
            enemies.add(en)
            all_sprites.add(en)
            
        # Spawn goal
        g = level_data["goal"]
        goal = Goal(g[0], g[1], g[2], g[3])
        goals.add(goal)
        all_sprites.add(goal)
        
        # Spawn player
        start_pos = level_data["start"]
        player = Ninja(start_pos[0], start_pos[1], duo, env_color)
        all_sprites.add(player)
        
        # Play environment music
        play_environment_music(level_index)

    def on_start():
        state_data["current_state"] = GameState.GAMEPLAY
        state_data["current_level"] = 0
        state_data["won"] = False
        load_level(0)

    btn_y = 530
    prev_btn = Button(150, btn_y, 100, 45, "< Prev", GRAY, BLACK, 24, on_prev)
    next_btn = Button(550, btn_y, 100, 45, "Next >", GRAY, BLACK, 24, on_next)
    rand_btn = Button(300, btn_y, 200, 45, "Randomize", GRAY, BLACK, 24, on_random)
    start_btn = Button(300, 465, 200, 50, "Start Mission", WHITE, BLACK, 28, on_start)
    
    buttons = [prev_btn, next_btn, rand_btn, start_btn]
    
    # Generate character selection grid buttons dynamically!
    grid_x_start = 70
    grid_y_start = 110
    button_w = 120
    button_h = 40
    spacing_x = 135
    spacing_y = 50
    
    char_buttons = []
    for idx, char in enumerate(ROSTER):
        row = idx // 5
        col = idx % 5
        bx = grid_x_start + col * spacing_x
        by = grid_y_start + row * spacing_y
        
        def make_callback(val=idx):
            state_data["selected_index"] = val
            
        btn = Button(bx, by, button_w, button_h, char.name.split()[0], GRAY, BLACK, 20, make_callback)
        char_buttons.append(btn)
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle UI events
            if state_data["current_state"] == GameState.SELECTION:
                for btn in buttons:
                    btn.handle_event(event)
                for btn in char_buttons:
                    btn.handle_event(event)

            # Basic state transitions for testing purposes
            if event.type == pygame.KEYDOWN:
                if state_data["current_state"] == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        state_data["current_state"] = GameState.SELECTION
                elif state_data["current_state"] == GameState.GAMEPLAY:
                    if event.key == pygame.K_x:
                        state_data["current_state"] = GameState.GAME_OVER
                        stop_music()
                    elif event.key in (pygame.K_c, pygame.K_LSHIFT, pygame.K_RSHIFT):
                        player.switch_ninja()
                        spawn_switch_burst(player.rect.center, player.duo.element)
                elif state_data["current_state"] == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        state_data["current_state"] = GameState.MENU
                        
        # Render
        screen.fill(BLACK)
        
        # Draw current state
        if state_data["current_state"] == GameState.MENU:
            text = font.render("MENU - Press SPACE to Start", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            
        elif state_data["current_state"] == GameState.SELECTION:
            # Draw Selection Screen
            title_text = title_font.render("SELECT YOUR CHARACTER", True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 35))
            
            # Draw character buttons grid
            for idx, btn in enumerate(char_buttons):
                if idx == state_data["selected_index"]:
                    btn.bg_color = (255, 140, 0) # Highlight selected character
                    btn.text_color = WHITE
                else:
                    btn.bg_color = (80, 80, 80) # Dark gray base
                    btn.text_color = WHITE
                btn.draw(screen)
                
            char = ROSTER[state_data["selected_index"]]
            
            # Character Info
            name_text = font.render(char.name, True, (255, 69, 0)) # RedOrange
            screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, 240))
            
            elem_text = desc_font.render(f"Element: {char.element}", True, (200, 200, 200))
            screen.blit(elem_text, (WIDTH//2 - elem_text.get_width()//2, 300))
            
            desc_text = desc_font.render(char.description, True, WHITE)
            screen.blit(desc_text, (WIDTH//2 - desc_text.get_width()//2, 360))
            
            # Draw bottom action buttons
            for btn in buttons:
                btn.draw(screen)
                
        elif state_data["current_state"] == GameState.GAMEPLAY:
            # Update physics
            player.update(platforms)
            enemies.update(platforms)
            
            # Check Goal Collision
            if pygame.sprite.spritecollideany(player, goals):
                state_data["current_level"] += 1
                if state_data["current_level"] < len(LEVELS):
                    load_level(state_data["current_level"])
                else:
                    state_data["won"] = True
                    state_data["current_state"] = GameState.GAME_OVER
                    stop_music()
                    
            # Check Obstacle Collision
            if pygame.sprite.spritecollideany(player, obstacles):
                state_data["won"] = False
                state_data["current_state"] = GameState.GAME_OVER
                stop_music()
                
            # Check Enemy Collision
            enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
            for enemy in enemy_hits:
                # Stomp logic: falling down onto the enemy's head
                if player.velocity.y > 0 and player.rect.bottom < enemy.rect.centery + 10:
                    enemy.kill() # Destroy enemy
                    player.velocity.y = player.jump_power * 0.8 # Small bounce
                else:
                    state_data["won"] = False
                    state_data["current_state"] = GameState.GAME_OVER
                    stop_music()
                
            # Check falling off screen
            if player.rect.y > HEIGHT:
                state_data["won"] = False
                state_data["current_state"] = GameState.GAME_OVER
                stop_music()
            
            # Draw game world
            if active_bg:
                screen.blit(active_bg, (0, 0))
            else:
                env_name, env_color = get_env_for_level(state_data["current_level"])
                duo = ROSTER[state_data["selected_index"]]
                elem_color = ELEMENT_COLORS.get(duo.element, (255, 255, 255))
                bg_fill_color = (
                    int(env_color[0] * 0.2 + elem_color[0] * 0.1),
                    int(env_color[1] * 0.2 + elem_color[1] * 0.1),
                    int(env_color[2] * 0.2 + elem_color[2] * 0.1)
                )
                screen.fill(bg_fill_color)
                
            # Draw particles behind characters and platforms
            update_and_draw_particles(screen)
            
            # Spawn level particles
            duo = ROSTER[state_data["selected_index"]]
            spawn_level_particles(state_data["current_level"], duo.element)
                
            all_sprites.draw(screen)
            
            # Draw HUD
            active_ninja_name = player.get_active_name()
            env_name, _ = get_env_for_level(state_data["current_level"])
            text = font.render(f"Player: {active_ninja_name} - Level {state_data['current_level'] + 1}", True, WHITE)
            screen.blit(text, (10, 10))
            
            text2 = desc_font.render(f"Region: {env_name} | Press C/SHIFT for Chakra Burst!", True, GRAY)
            screen.blit(text2, (10, 50))
            
        elif state_data["current_state"] == GameState.GAME_OVER:
            if state_data["won"]:
                text = font.render("YOU WIN! - Press R to Restart", True, (0, 255, 0))
            else:
                text = font.render("GAME OVER - Press R to Restart", True, RED)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            
        pygame.display.flip()
        
        # Maintain frame rate
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
