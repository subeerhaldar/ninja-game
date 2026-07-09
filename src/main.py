import pygame
import sys
import random
from game_state import GameState
from roster import ROSTER
from ui import Button
from player import Ninja, Platform, Goal, Obstacle, Enemy
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
        bg_image = pygame.image.load("assets/bg.png").convert()
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    except:
        bg_image = None
    
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
        nonlocal player
        all_sprites.empty()
        platforms.empty()
        goals.empty()
        obstacles.empty()
        enemies.empty()
        
        level_data = LEVELS[level_index]
        
        # Spawn platforms
        for p in level_data["platforms"]:
            plat = Platform(p[0], p[1], p[2], p[3])
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
        duo = ROSTER[state_data["selected_index"]]
        start_pos = level_data["start"]
        player = Ninja(start_pos[0], start_pos[1], duo.element)
        all_sprites.add(player)

    def on_start():
        state_data["current_state"] = GameState.GAMEPLAY
        state_data["current_level"] = 0
        state_data["won"] = False
        load_level(0)

    btn_y = 500
    prev_btn = Button(150, btn_y, 100, 50, "< Prev", GRAY, BLACK, 30, on_prev)
    next_btn = Button(550, btn_y, 100, 50, "Next >", GRAY, BLACK, 30, on_next)
    rand_btn = Button(300, btn_y, 200, 50, "Randomize", GRAY, BLACK, 30, on_random)
    start_btn = Button(300, btn_y - 70, 200, 50, "Start Mission", WHITE, BLACK, 30, on_start)
    
    buttons = [prev_btn, next_btn, rand_btn, start_btn]
    
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

            # Basic state transitions for testing purposes
            if event.type == pygame.KEYDOWN:
                if state_data["current_state"] == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        state_data["current_state"] = GameState.SELECTION
                elif state_data["current_state"] == GameState.GAMEPLAY:
                    if event.key == pygame.K_x:
                        state_data["current_state"] = GameState.GAME_OVER
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
            title_text = title_font.render("SELECT YOUR DUO", True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
            
            duo = ROSTER[state_data["selected_index"]]
            
            # Duo Info
            name_text = font.render(duo.name, True, RED)
            screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, 150))
            
            ninjas_text = desc_font.render(f"Ninjas: {duo.ninja_1} & {duo.ninja_2}", True, GRAY)
            screen.blit(ninjas_text, (WIDTH//2 - ninjas_text.get_width()//2, 220))
            
            elem_text = desc_font.render(f"Element: {duo.element}", True, GRAY)
            screen.blit(elem_text, (WIDTH//2 - elem_text.get_width()//2, 260))
            
            desc_text = desc_font.render(duo.description, True, WHITE)
            screen.blit(desc_text, (WIDTH//2 - desc_text.get_width()//2, 320))
            
            # Draw buttons
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
                    
            # Check Obstacle Collision
            if pygame.sprite.spritecollideany(player, obstacles):
                state_data["won"] = False
                state_data["current_state"] = GameState.GAME_OVER
                
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
                
            # Check falling off screen
            if player.rect.y > HEIGHT:
                state_data["won"] = False
                state_data["current_state"] = GameState.GAME_OVER
            
            # Draw game world
            if bg_image:
                screen.blit(bg_image, (0, 0))
                
            all_sprites.draw(screen)
            
            # Draw HUD
            duo = ROSTER[state_data["selected_index"]]
            text = font.render(f"Playing as: {duo.name} - Level {state_data['current_level'] + 1}", True, WHITE)
            screen.blit(text, (10, 10))
            
            text2 = desc_font.render("Reach the yellow Goal! Don't fall!", True, GRAY)
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
