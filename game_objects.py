"""
Game Objects Module
Defines Target, Obstacle, and PowerUp classes for the game.
"""

import pygame
import random
import math
import os
from typing import Tuple


class GameObject:
    """Base class for all game objects."""

    def __init__(self, x: int, y: int, radius: int, color: Tuple[int, int, int], speed: float):
        """
        Initialize game object.
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.active = True

    def update(self, dt: float):
        """Update object position."""
        pass  # To be overridden by subclasses

    def draw(self, surface: pygame.Surface):
        """Draw object on surface."""
        if self.active:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def get_position(self) -> Tuple[int, int]:
        """Get object center position."""
        return (int(self.x), int(self.y))


class Target(GameObject):
    """
    Target object that player should punch for points.
    Uses rotating images (poin_1.png, poin_2.png).
    """
    DEFAULT_RADIUS = 40
    SPEED_RANGE = (50, 150)  # (min_speed, max_speed)
    POINTS = 10
    COLOR = (0, 255, 0)  # Green (fallback if image not found)
    ROTATION_SPEED = 120  # Degrees per second
    
    # Class-level cache for loaded images
    _images_cache = {}
    _assets_dir = 'assets/images'

    def __init__(self, x: int, y: int, screen_width: int, screen_height: int):
        """
        Initialize Target with rotating image.
        """
        super().__init__(
            x, y,
            radius=self.DEFAULT_RADIUS,
            color=self.COLOR,
            speed=random.uniform(*self.SPEED_RANGE)  
        )
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.points = self.POINTS
        
        # Rotation
        self.angle = 0  # Current rotation angle
        
        # Load random poin image
        self.image = None
        self.original_image = None
        self._load_image()

    def _load_image(self):
        """Load a random poin image from assets."""
        # Choose random poin image (1 or 2)
        poin_num = random.randint(1, 2)
        image_name = f'poin_{poin_num}.png'
        
        # Check cache first
        if image_name in self._images_cache:
            self.original_image = self._images_cache[image_name]
            self.image = self.original_image.copy()
            return
        
        # Try to load image
        image_path = os.path.join(self._assets_dir, image_name)
        if os.path.exists(image_path):
            try:
                img = pygame.image.load(image_path).convert_alpha()
                # Scale to appropriate size (2x radius)
                size = self.radius * 2
                img = pygame.transform.smoothscale(img, (size, size))
                self._images_cache[image_name] = img
                self.original_image = img
                self.image = img.copy()
            except Exception as e:
                print(f"[Warning] Failed to load {image_name}: {e}")
                self.original_image = None
                self.image = None
        else:
            print(f"[Warning] Image not found: {image_path}")
            self.original_image = None
            self.image = None

    def update(self, dt: float):
        """Move target, bounce off walls, and rotate."""
        if not self.active:
            return

        # Move target
        self.x += self.direction_x * self.speed * dt
        self.y += self.direction_y * self.speed * dt

        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= self.screen_width:
            self.direction_x *= -1
            self.x = max(self.radius, min(self.x, self.screen_width - self.radius))

        if self.y - self.radius <= 0 or self.y + self.radius >= self.screen_height:
            self.direction_y *= -1
            self.y = max(self.radius, min(self.y, self.screen_height - self.radius))
        
        # Rotate image
        self.angle += self.ROTATION_SPEED * dt
        if self.angle >= 360:
            self.angle -= 360
        
        # Update rotated image
        if self.original_image:
            self.image = pygame.transform.rotate(self.original_image, self.angle)

    def draw(self, surface: pygame.Surface):
        """Draw rotating target image."""
        if not self.active:
            return
        
        if self.image:
            # Get rect and center it on position
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image, rect)
        else:
            # Fallback to circle with bullseye if image not loaded
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius // 2)
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 5)


class Obstacle(GameObject):
    """
    Obstacle object that damages player if hit.
    Uses rotating images (hit_1.png, hit_2.png, hit_3.png).
    """
    DEFAULT_RADIUS = 50
    SPEED_RANGE = (80, 200)
    COLOR = (255, 0, 0)  # Red (fallback if image not found)
    DAMAGE = 20
    LIVES_COST = 1
    LIFETIME = 10.0  # Seconds
    DEACTIVATE_DISTANCE = 50  # Distance from target to deactivate
    ROTATION_SPEED = 360  # Degrees per second
    
    # Class-level cache for loaded images
    _images_cache = {}
    _assets_dir = 'assets/images'

    def __init__(self, x: int, y: int, screen_width: int, screen_height: int):
        """
        Initialize Obstacle with rotating image.
        """
        super().__init__(
            x, y,
            radius=self.DEFAULT_RADIUS,
            color=self.COLOR,
            speed=random.uniform(*self.SPEED_RANGE)
        )
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.damage = self.DAMAGE
        self.lives_cost = self.LIVES_COST
        self.time_alive = 0
        
        # Target position (center of screen with randomness)
        self.target_x = self.screen_width // 2 + random.randint(-100, 100)
        self.target_y = self.screen_height // 2 + random.randint(-100, 100)
        
        # Rotation
        self.angle = 0  # Current rotation angle
        
        # Load random hit image
        self.image = None
        self.original_image = None
        self._load_image()

    def _load_image(self):
        """Load a random hit image from assets."""
        # Choose random hit image (1 or 2)
        hit_num = random.randint(1, 2)
        image_name = f'hit_{hit_num}.png'
        
        # Check cache first
        if image_name in self._images_cache:
            self.original_image = self._images_cache[image_name]
            self.image = self.original_image.copy()
            return
        
        # Try to load image
        image_path = os.path.join(self._assets_dir, image_name)
        if os.path.exists(image_path):
            try:
                img = pygame.image.load(image_path).convert_alpha()
                # Scale to appropriate size (2x radius)
                size = self.radius * 2
                img = pygame.transform.smoothscale(img, (size, size))
                self._images_cache[image_name] = img
                self.original_image = img
                self.image = img.copy()
            except Exception as e:
                print(f"[Warning] Failed to load {image_name}: {e}")
                self.original_image = None
                self.image = None
        else:
            print(f"[Warning] Image not found: {image_path}")
            self.original_image = None
            self.image = None

    def update(self, dt: float):
        """Move obstacle towards target and rotate."""
        if not self.active:
            return

        # Update lifetime
        self.time_alive += dt
        if self.time_alive >= self.LIFETIME:
            self.active = False
            return

        # Calculate distance to target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        # Deactivate if reached target
        if distance < self.DEACTIVATE_DISTANCE:
            self.active = False
            return

        # Move towards target
        if distance > 0:
            self.x += (dx / distance) * self.speed * dt
            self.y += (dy / distance) * self.speed * dt
        
        # Rotate image
        self.angle += self.ROTATION_SPEED * dt
        if self.angle >= 360:
            self.angle -= 360
        
        # Update rotated image
        if self.original_image:
            self.image = pygame.transform.rotate(self.original_image, self.angle)

    def draw(self, surface: pygame.Surface):
        """Draw rotating obstacle image."""
        if not self.active:
            return
        
        if self.image:
            # Get rect and center it on position
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image, rect)
        else:
            # Fallback to circle with X if image not loaded
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.line(
                surface, (255, 255, 255),
                (int(self.x - 10), int(self.y - 10)),
                (int(self.x + 10), int(self.y + 10)), 3
            )
            pygame.draw.line(
                surface, (255, 255, 255),
                (int(self.x + 10), int(self.y - 10)),
                (int(self.x - 10), int(self.y + 10)), 3
            )


class PowerUp(GameObject):
    """
    Power-up object that gives player bonus.
    """
    TYPES = ['shield', 'double_score', 'slow_motion']
    DEFAULT_RADIUS = 20
    COLOR = (255, 255, 0)  # Yellow
    SPEED = 100  
    LIFETIME = 5.0  # Seconds

    def __init__(self, x: int, y: int, screen_width: int, screen_height: int):
        """
        Initialize PowerUp.
        """
        super().__init__(
            x, y,
            radius=self.DEFAULT_RADIUS,
            color=self.COLOR,
            speed=self.SPEED
        )
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.type = random.choice(self.TYPES)
        self.time_alive = 0

    def update(self, dt: float):
        """Update power-up (floating effect)."""
        if not self.active:
            return

        self.time_alive += dt
        if self.time_alive >= self.LIFETIME:
            self.active = False
            return

        # Floating effect (sine wave)
        self.y += math.sin(self.time_alive * 3) * 2

    def draw(self, surface: pygame.Surface):
        """Draw power-up with star effect."""
        if self.active:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            
            # Star points
            points = []
            for i in range(5):
                angle = math.pi * 2 * i / 5 - math.pi / 2
                px = self.x + math.cos(angle) * (self.radius - 5)
                py = self.y + math.sin(angle) * (self.radius - 5)
                points.append((int(px), int(py)))
            if len(points) >= 3:
                pygame.draw.polygon(surface, (255, 165, 0), points)