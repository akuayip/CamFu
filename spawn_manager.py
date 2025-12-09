"""
Spawn Manager Module
Handles all logic for spawning game objects.
"""
import random
from game_objects import Target, Obstacle, PowerUp

class SpawnManager:
    """
    Manages the timing and logic for spawning all game objects.
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize the spawn manager.
        Args:
            screen_width: Width of the game screen.
            screen_height: Height of the game screen.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Timers for spawning
        self.target_spawn_timer = 0
        self.target_spawn_interval = 3.0  # Spawn target every 3 seconds
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_interval = 5.0  # Spawn obstacle every 5 seconds
        self.powerup_spawn_timer = 0
        self.powerup_spawn_interval = 15.0  # Spawn powerup every 15 seconds

    def update_screen_size(self, w, h):
        """Update screen dimensions when window is resized."""
        self.screen_width = w
        self.screen_height = h

    def update(self, dt, targets, obstacles, powerups):
        """
        Update spawn timers and create new objects if ready.
        
        Args:
            dt: Delta time.
            targets: The main list of target objects.
            obstacles: The main list of obstacle objects.
            powerups: The main list of powerup objects.
        """
        # Update spawn timers
        self.target_spawn_timer += dt
        self.obstacle_spawn_timer += dt
        self.powerup_spawn_timer += dt

        # Spawn objects
        if self.target_spawn_timer >= self.target_spawn_interval:
            self.spawn_target(targets)
            self.target_spawn_timer = 0

        if self.obstacle_spawn_timer >= self.obstacle_spawn_interval:
            self.spawn_obstacle(obstacles)
            self.obstacle_spawn_timer = 0

        if self.powerup_spawn_timer >= self.powerup_spawn_interval:
            self.spawn_powerup(powerups)
            self.powerup_spawn_timer = 0
            
    def reset_timers(self):
        """Resets all spawn timers."""
        self.target_spawn_timer = 0
        self.obstacle_spawn_timer = 0
        self.powerup_spawn_timer = 0

    def spawn_target(self, targets):
        """Spawn a new target and add it to the list."""
        x = random.randint(100, self.screen_width - 100)
        y = random.randint(100, self.screen_height - 100)
        targets.append(Target(x, y, self.screen_width, self.screen_height))

    def spawn_obstacle(self, obstacles):
        """Spawn a new obstacle from random edge and add it to the list."""
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        
        if edge == 'top':
            x = random.randint(0, self.screen_width)
            y = -50
        elif edge == 'bottom':
            x = random.randint(0, self.screen_width)
            y = self.screen_height + 50
        elif edge == 'left':
            x = -50
            y = random.randint(0, self.screen_height)
        else:  # right
            x = self.screen_width + 50
            y = random.randint(0, self.screen_height)
        
        obstacles.append(Obstacle(x, y, self.screen_width, self.screen_height))

    def spawn_powerup(self, powerups):
        """Spawn a new power-up and add it to the list."""
        x = random.randint(100, self.screen_width - 100)
        y = random.randint(100, self.screen_height - 100)
        powerups.append(PowerUp(x, y, self.screen_width, self.screen_height))