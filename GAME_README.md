# Cam-Fu Game - README

## 🎮 Tentang Game

**Cam-Fu** adalah game interaktif berbasis pose detection menggunakan webcam. Gunakan tubuh Anda sebagai controller untuk:

- 👊 **PUNCH** target hijau untuk mendapat poin
- 🤺 **DODGE** obstacle merah yang menyerang
- ⭐ **GRAB** power-up kuning untuk bonus

## 🎯 Cara Bermain

### Objek Game:

1. **🎯 Target (Hijau)**

   - Pukul dengan tangan untuk +10 poin
   - Bergerak memantul di layar

2. **💥 Obstacle (Merah)**

   - HINDARI! Akan mengurangi HP dan score
   - Bergerak mendekat ke player
   - -20 poin & -1 HP jika kena

3. **⭐ Power-Up (Kuning)**
   - Ambil dengan tangan untuk bonus
   - Hilang setelah 5 detik
   - Tipe:
     - 🛡️ **Shield**: Proteksi dari damage (5s)
     - ⚡ **Double Score**: 2x poin (8s)
     - 🐌 **Slow Motion**: Perlambat objek (6s)

### Kontrol:

- **SPACE** - Pause/Resume
- **C** - Toggle camera view
- **R** - Restart (saat game over)
- **ESC / Q** - Keluar dari game

## 🚀 Instalasi & Menjalankan Game

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Game

```bash
python main_game.py
```

Atau untuk pose detection saja (tanpa game):

```bash
python main.py
```

## 📁 Struktur File Game

```
CamFu/
├── main.py                # Entry point game
├── game_engine.py         # Game loop & rendering
├── pose_detector.py       # Pose detection (MediaPipe)
├── collision_detector.py  # Collision detection logic
├── game_objects.py        # Target, Obstacle, PowerUp
├── score_manager.py       # Score, lives, power-ups
├── sound_manager.py       # Sound effects & music
├── assets/
│   ├── sounds/           # Sound effects (auto-generated)
│   └── images/           # Images (placeholder)
└── requirements.txt       # Dependencies
```

## 🎨 Fitur Game

✅ Real-time pose detection dengan MediaPipe  
✅ Collision detection antara pose & objek  
✅ System score & lives  
✅ Power-up system (Shield, 2x Score, Slow-Mo)  
✅ Sound effects (auto-generated jika file tidak ada)  
✅ Pause/Resume game  
✅ Game over & restart

## 🛠️ Troubleshooting

### Pygame tidak terinstall

```bash
pip install pygame>=2.5.0
```

### Sound tidak keluar

Sound effects akan auto-generate jika file `.wav` tidak ada di `assets/sounds/`. Ini normal!

### Camera lag

- Turunkan FPS di `game_engine.py` (baris `self.fps = 60` menjadi `30`)
- Gunakan `model_complexity=0` untuk pose detection yang lebih cepat

### Objek terlalu cepat

Edit di `game_objects.py`:

- `Target`: Ubah `speed=random.uniform(50, 150)` menjadi lebih kecil
- `Obstacle`: Ubah `speed=random.uniform(80, 200)` menjadi lebih kecil

## 🎮 Tips Bermain

1. **Posisi Optimal**: Berdiri 1.5-2 meter dari kamera
2. **Pencahayaan**: Pastikan ruangan cukup terang
3. **Gerakan**: Gunakan gerakan punch yang jelas untuk hit target
4. **Strategi**: Prioritas dodge obstacle > punch target

## 📊 Scoring

- Hit target: **+10 poin** (x2 saat Double Score aktif)
- Kena obstacle: **-20 poin & -1 HP**
- Game over: **0 HP**
- High score tersimpan selama sesi game

## 🔊 Sound Effects

Game akan generate sound effects sederhana jika file audio tidak ada:

- **Hit**: High pitch beep (A5 - 880Hz)
- **Damage**: Low pitch beep (A3 - 220Hz)
- **Power-up**: Very high beep (E6 - 1320Hz)
- **Game Over**: Very low beep (A2 - 110Hz)

Anda bisa menambahkan file `.wav` custom ke `assets/sounds/`:

- `hit.wav`
- `damage.wav`
- `powerup.wav`
- `game_over.wav`
- `level_up.wav`

## 🎯 Pengembangan Selanjutnya

Fitur yang bisa ditambahkan:

- [ ] Multiple levels dengan kesulitan berbeda
- [ ] Boss fights
- [ ] Combo system
- [ ] Leaderboard online
- [ ] Custom character/skin
- [ ] Multiplayer mode
- [ ] Gesture recognition untuk special moves

## 👥 Credits

Developed by Kelompok Mulmed-Ceria:

- Cindy Nadila Putri (122140002)
- M. Arief Rahman Hakim (122140083)
- Zidan Raihan (122140100)

---

**Selamat Bermain! 🥋**
