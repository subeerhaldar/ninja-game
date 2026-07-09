# Level definitions

LEVELS = [
    # Level 1
    {
        "platforms": [
            (0, 560, 800, 40), # Floor
            (200, 450, 150, 20),
            (500, 350, 150, 20),
            (380, 220, 100, 20),
        ],
        "obstacles": [],
        "goal": (410, 160, 40, 60), # At top platform
        "start": (100, 450)
    },
    # Level 2
    {
        "platforms": [
            (0, 560, 800, 40), # Floor
            (150, 480, 100, 20),
            (350, 410, 100, 20),
            (550, 340, 100, 20),
            (350, 260, 100, 20), # Intermediate step to get back left
            (150, 180, 150, 20), # Final platform
        ],
        "obstacles": [],
        "goal": (200, 120, 40, 60),
        "start": (50, 450)
    },
    # Level 3
    {
        "platforms": [
            (0, 560, 800, 40), # Solid Floor (no holes)
            (300, 460, 100, 20), # Step 1 
            (150, 360, 100, 20), # Step 2
            (350, 260, 100, 20), # Step 3
            (550, 160, 100, 20)  # Step 4
        ],
        "obstacles": [],
        "goal": (580, 100, 40, 60),
        "start": (50, 450)
    },
    # Level 4 (Death pit intro)
    {
        "platforms": [
            (0, 560, 200, 40), # Larger starting floor
            (200, 460, 120, 20),
            (350, 460, 120, 20),
            (500, 360, 120, 20),
            (350, 260, 120, 20),
            (200, 160, 120, 20),
            (50, 160, 120, 20)
        ],
        "obstacles": [
            (150, 540, 40, 20) # Just a small spike on the ground
        ],
        "enemies": [
            (350, 200) # One enemy on a high platform
        ],
        "goal": (80, 100, 40, 60),
        "start": (50, 450)
    },
    # Level 5 (The Tall Climb)
    {
        "platforms": [
            (0, 560, 300, 40), # Bigger start floor
            (250, 500, 150, 20), 
            (450, 440, 150, 20),
            (650, 380, 150, 20),
            (450, 300, 150, 20),
            (250, 220, 150, 20),
            (50, 160, 200, 20), # Huge Goal platform
        ],
        "obstacles": [
            (400, 540, 100, 20) # Lava pit on the ground
        ],
        "enemies": [
            (450, 350),
            (250, 130)
        ],
        "goal": (100, 100, 40, 60),
        "start": (50, 450)
    },
    # Level 6 (The Ascending Bridge)
    {
        "platforms": [
            (0, 560, 200, 40), # Start floor
            (250, 480, 120, 20),
            (420, 400, 120, 20),
            (590, 320, 120, 20),
            (420, 240, 120, 20),
            (250, 160, 120, 20),
            (80, 100, 150, 20)
        ],
        "obstacles": [
            (300, 540, 100, 20), # Lava pit on the ground
            (600, 540, 100, 20)
        ],
        "enemies": [
            (420, 310),
            (590, 230)
        ],
        "goal": (130, 40, 40, 60),
        "start": (50, 450)
    },
    # Level 7 (The Final Climb)
    {
        "platforms": [
            (0, 560, 150, 40), # Start
            (200, 480, 120, 20),
            (370, 400, 120, 20),
            (540, 320, 120, 20),
            (680, 240, 120, 20),
            (540, 160, 120, 20),
            (370, 120, 120, 20),
            (200, 80, 120, 20),
        ],
        "obstacles": [
            (300, 540, 50, 20), # Small lava pits on ground
            (500, 540, 50, 20),
            (700, 540, 50, 20)
        ],
        "enemies": [
            (370, 310),
            (540, 70)
        ],
        "goal": (240, 20, 40, 60),
        "start": (50, 450)
    }
]

# Programmatically generate Levels 8 through 15
import random

for i in range(8, 16):
    random.seed(i) # Ensure levels are the same every time we run
    
    platforms = [
        (0, 560, 800, 40) # Safe solid floor
    ]
    
    # Generate an easy zig-zag pattern upwards
    cur_x = 50
    cur_y = 480
    
    for step in range(5):
        # Move up a tiny bit, and only move left/right slightly so jumps are never too far!
        cur_x += random.randint(-150, 150)
        # Keep it on the screen
        cur_x = max(50, min(550, cur_x))
        
        cur_y -= random.randint(40, 70) # Very small vertical jump
        platforms.append((cur_x, cur_y, 200, 20)) # Massive 200px wide platforms
        
    # Place goal on the very last platform we generated
    goal = (cur_x + 50, cur_y - 60, 40, 60)
    
    # Add a random lava pit on the ground floor
    obstacles = [
        (random.randint(200, 600), 540, 50, 20)
    ]
    
    enemies = [
        (cur_x, cur_y - 80) # One enemy near the top
    ]
    
    LEVELS.append({
        "platforms": platforms,
        "obstacles": obstacles,
        "enemies": enemies,
        "goal": goal,
        "start": (50, 450)
    })
