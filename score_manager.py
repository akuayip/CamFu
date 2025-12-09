"""
Score Manager Module
Handles score, lives, levels, and power-up states.
"""

import time


class ScoreManager:
    """
    Tracks score, lives, level progression, and temporary power-ups.
    """

    def __init__(self, starting_lives=3):
        self.score = 0
        self.lives = starting_lives
        self.max_lives = starting_lives
        self.high_score = 0

        self.game_over = False
        self.game_won = False
        self.level = 1

        # Power-up states
        self.shield_active = False
        self.shield_duration = 0
        self.double_score_active = False
        self.double_score_duration = 0
        self.slow_motion_active = False
        self.slow_motion_duration = 0

        # Stats
        self.targets_hit = 0
        self.obstacles_dodged = 0
        self.start_time = time.time()

    def add_score(self, points: int, sound_manager=None):
        """
        Add points (affected by double-score power-up).
        Handles automatic level-up every 500 points.
        """
        multiplier = 2 if self.double_score_active else 1
        old_score = self.score

        self.score += points * multiplier

        # Level up check
        if (old_score // 500) < (self.score // 500):
            self.level += 1
            if sound_manager:
                sound_manager.play_sound('level_up')

        if self.score > self.high_score:
            self.high_score = self.score

    def subtract_score(self, points: int):
        """Reduce score without going below zero."""
        self.score = max(0, self.score - points)

    def lose_life(self, sound_manager):
        """
        Remove 1 life unless shield is active.
        Returns True if damage was applied.
        """
        if self.shield_active:
            return False

        self.lives -= 1

        if self.lives <= 0:
            self.game_over = True
            if sound_manager:
                sound_manager.play_sound('game_over')
        else:
            if sound_manager:
                sound_manager.play_sound('damage')

        return True

    def add_life(self):
        """Increase life (not exceeding max)."""
        self.lives = min(self.max_lives, self.lives + 1)

    def activate_powerup(self, powerup_type: str):
        """
        Enable a power-up with its duration.
        Types: 'shield', 'double_score', 'slow_motion'
        """
        if powerup_type == 'shield':
            self.shield_active = True
            self.shield_duration = 5.0
        elif powerup_type == 'double_score':
            self.double_score_active = True
            self.double_score_duration = 8.0
        elif powerup_type == 'slow_motion':
            self.slow_motion_active = True
            self.slow_motion_duration = 6.0

    def update(self, dt: float):
        """Update power-up timers."""
        if self.shield_active:
            self.shield_duration -= dt
            if self.shield_duration <= 0:
                self.shield_active = False

        if self.double_score_active:
            self.double_score_duration -= dt
            if self.double_score_duration <= 0:
                self.double_score_active = False

        if self.slow_motion_active:
            self.slow_motion_duration -= dt
            if self.slow_motion_duration <= 0:
                self.slow_motion_active = False

    def reset(self):
        """Reset all game stats and power-ups."""
        self.score = 0
        self.lives = self.max_lives
        self.game_over = False
        self.game_won = False
        self.level = 1

        self.targets_hit = 0
        self.obstacles_dodged = 0

        self.shield_active = False
        self.double_score_active = False
        self.slow_motion_active = False

        self.start_time = time.time()

    def get_play_time(self) -> str:
        """Return total play time formatted as MM:SS."""
        elapsed = int(time.time() - self.start_time)
        return f"{elapsed // 60:02d}:{elapsed % 60:02d}"

    def get_stats(self) -> dict:
        """Return all gameplay statistics."""
        return {
            'score': self.score,
            'high_score': self.high_score,
            'lives': self.lives,
            'targets_hit': self.targets_hit,
            'obstacles_dodged': self.obstacles_dodged,
            'play_time': self.get_play_time(),
            'level': self.level
        }
