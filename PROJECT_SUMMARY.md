# Cam-Fu - Project Summary

## 🎮 Overview

Cam-Fu adalah game interaktif berbasis pose detection menggunakan webcam. Gunakan tubuh Anda untuk punch targets, dodge obstacles, dan grab power-ups!

## 📦 Files & Modules

### Core Files (Required)

1. **main.py** (Entry Point)

   - Main entry point untuk menjalankan game
   - Handle camera selection
   - Initialize GameEngine

2. **game_engine.py** (Game Loop)

   - Main game loop dengan Pygame
   - Rendering semua game objects
   - Handle events (pause, restart, quit)
   - Pose detection integration
   - Collision detection coordination

3. **pose_detector.py** (Pose Detection)

   - MediaPipe pose detection wrapper
   - Convert landmarks to pixel coordinates
   - Detect 33 body landmarks

4. **collision_detector.py** (Collision Logic)

   - Detect collision antara landmarks & objects
   - Check hand collision (punch targets/grab powerups)
   - Check body collision (hit by obstacles)

5. **game_objects.py** (Game Objects)

   - Target class (green circles, +10 points)
   - Obstacle class (red circles, damage player)
   - PowerUp class (yellow circles, bonuses)

6. **score_manager.py** (Game State)

   - Track score, lives, game over
   - Manage power-up states
   - Game statistics

7. **sound_manager.py** (Audio)
   - Load/play sound effects
   - Auto-generate beep sounds if files missing
   - Background music support

### Configuration Files

- **requirements.txt** - Python dependencies
- **.gitignore** - Ignore pycache

### Documentation

- **README.md** - Setup & installation
- **GAME_README.md** - Gameplay guide

### Assets (Optional)

- **assets/sounds/** - Sound effects (auto-generated if missing)
- **assets/images/** - Game images (using pygame shapes)

## 🚀 Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
python main.py
```

## 🎯 Game Mechanics

### Objects:

- 🎯 **Target (Green)**: Punch untuk +10 poin
- 💥 **Obstacle (Red)**: Dodge! -20 poin & -1 HP
- ⭐ **PowerUp (Yellow)**: Grab untuk bonus

### Power-ups:

- 🛡️ Shield (5s): Proteksi dari damage
- ⚡ Double Score (8s): 2x poin
- 🐌 Slow Motion (6s): Perlambat objects

### Controls:

- **SPACE**: Pause/Resume
- **C**: Toggle camera view
- **R**: Restart (game over)
- **ESC/Q**: Quit

## 🔧 Technical Stack

- Python 3.10+
- OpenCV (video capture)
- MediaPipe (pose detection)
- Pygame (game engine)
- NumPy (array ops)

## 📊 Code Statistics

- Total files: 7 Python modules
- Lines of code: ~1500+
- Main game loop: 60 FPS
- Pose landmarks: 33 points
- Collision radius: 25 pixels

## 🎨 Architecture

```
main.py
  └─> GameEngine
       ├─> PoseDetector (pose detection)
       ├─> CollisionDetector (collision logic)
       ├─> ScoreManager (game state)
       ├─> SoundManager (audio)
       └─> Game Objects
            ├─> Target (spawn every 3s)
            ├─> Obstacle (spawn every 5s)
            └─> PowerUp (spawn every 15s)
```

## 🚧 Future Enhancements

- [ ] Multiple levels
- [ ] Boss fights
- [ ] Combo system
- [ ] Online leaderboard
- [ ] Custom skins
- [ ] Multiplayer mode
- [ ] Special moves (gesture recognition)

## 👥 Team

Kelompok Mulmed-Ceria:

- Cindy Nadila Putri (122140002)
- M. Arief Rahman Hakim (122140083)
- Zidan Raihan (122140100)

---

Last updated: November 4, 2025
