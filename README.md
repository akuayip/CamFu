<div align="center">

# 🥋 Cam-Fu

<img src="assets/images/icon.png" alt="Cam-Fu Logo" width="200"/>

### Pose Fighting Game

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-fitur-utama) • [Installation](#-instalasi) • [How to Play](#-cara-bermain) • [Team](#-tim-pengembang) • [Logbook](#-logbook-mingguan)

</div>

---

## 📖 Tentang Project

**Cam-Fu** adalah game interaktif inovatif yang mengubah webcam biasa menjadi controller game berbasis gerakan tubuh! Rasakan sensasi menjadi petarung kungfu digital dengan teknologi **pose detection** real-time menggunakan MediaPipe dan OpenCV.

### 🎮 Konsep Game

> **Tinju, Hindari, Bertahan!**

- **🎯 Punch Targets**: Pukul target melayang untuk mendapatkan skor
- **⚠️ Dodge Obstacles**: Hindari rintangan yang bisa mengurangi nyawa
- **💪 Grab Powerups**: Ambil power-up untuk keuntungan strategis
- **🏆 High Score**: Bertahan selama mungkin dan raih skor tertinggi!

Game ini menggunakan deteksi pose full-body dan hand gesture recognition untuk menciptakan pengalaman bermain yang immersive, seperti VR tanpa perlu perangkat tambahan!

---

## ✨ Fitur Utama

### 🎥 Real-Time Pose Detection

- **Full Body Tracking** dengan MediaPipe Pose
- **Hand Gesture Recognition** untuk deteksi tinju (fist/open hand)
- **Collision Detection** akurat antara tangan dan objek game

### 🎨 Visual & Audio

- **Stickman Rendering** dari pose landmarks
- **Dynamic UI** dengan score, lives, dan power-up indicators
- **Background Music** & sound effects
- **Countdown Animation** sebelum game dimulai

### 🎯 Gameplay Features

- **Multiple Object Types**: Targets, Obstacles, Power-ups
- **Power-Up System**: Shield, Double Score, Slow Motion
- **Difficulty Scaling**: Spawn rate meningkat seiring waktu

---

## 👥 Tim Pengembang

<table>
<tr>
<td align="center">
<a href="https://github.com/cindynadilaptr">
<img src="https://github.com/cindynadilaptr.png" width="100px;" alt="Cindy Nadila Putri"/><br />
<sub><b>Cindy Nadila Putri</b></sub><br />
<sub>122140002</sub>
</a>
</td>
<td align="center">
<a href="https://github.com/akuayip">
<img src="https://github.com/akuayip.png" width="100px;" alt="M. Arief Rahman Hakim"/><br />
<sub><b>M. Arief Rahman Hakim</b></sub><br />
<sub>122140083</sub>
</a>
</td>
<td align="center">
<a href="https://github.com/zidbytes">
<img src="https://github.com/zidbytes.png" width="100px;" alt="Zidan Raihan"/><br />
<sub><b>Zidan Raihan</b></sub><br />
<sub>122140100</sub>
</a>
</td>
</tr>
</table>

---

## 📅 Logbook Mingguan

<details>
<summary><b>📊 Lihat Progress Lengkap</b></summary>

| Minggu | Periode              | 📝 Progress & Update                                                                                                   |
| :----: | -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **1**  | 28 Okt - 2 Nov 2025  | ✅ Membuat repository GitHub<br>✅ Brainstorming ide project game berbasis webcam                                      |
| **2**  | 4 Nov - 9 Nov 2025   | ✅ Menambahkan asset untuk game<br>✅ Refactor sistem collision detection<br>✅ Implementasi body landmark to stickman |
| **3**  | 11 Nov - 16 Nov 2025 | ✅ Implementasi main menu dengan gesture control                                                                       |
| **4**  | 18 Nov - 23 Nov 2025 | ✅ Refactor collision detection pada kepala<br>✅ Implementasi hand landmark untuk deteksi buka/tutup tangan           |
| **5**  | 25 Nov - 30 Nov 2025 |                                                                                                                        |

</details>

---

## 🚀 Instalasi

### 📋 Prasyarat

Pastikan sistem Anda memiliki:

- ✅ **Python 3.10 atau 3.11** (MediaPipe belum support Python 3.12+)
- ✅ **Webcam** (built-in atau external)
- ✅ **Git** untuk clone repository
- ✅ **Anaconda/Miniconda** (recommended) atau Python virtual environment

### 🔧 Langkah Instalasi

#### 1️⃣ Clone Repository

```bash
git clone https://github.com/akuayip/Mulmed-Ceria.git
cd Mulmed-Ceria
```

#### 2️⃣ Setup Python Environment

<details>
<summary><b>📦 Metode A: Menggunakan Anaconda (Recommended)</b></summary>

```bash
# Buat environment baru dengan Python 3.10
conda create -n camfu python=3.10 -y

# Aktifkan environment
conda activate camfu

# Install dependencies
pip install -r requirements.txt
```

</details>

<details>
<summary><b>⚡ Metode B: Menggunakan UV (Fast Package Manager)</b></summary>

```bash
# Install uv
pip install uv

# Buat virtual environment
uv venv --python 3.10

# Aktifkan environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

</details>

#### 3️⃣ Jalankan Game

**Windows:**

```bash
# Pastikan environment aktif
conda activate camfu

# Jalankan game
python main.py

# Atau gunakan batch file
run_game.bat
```

**Linux/Mac:**

```bash
# Aktivasi environment
source .venv/bin/activate  # atau: conda activate camfu

# Jalankan game
python main.py
```

---

## 🎮 Cara Bermain

### 🕹️ Controls

| Aksi                 | Cara                                                 |
| -------------------- | ---------------------------------------------------- |
| **Tinju Target**     | Kepalkan tangan (buat kepalan) dan arahkan ke target |
| **Hindari Obstacle** | Gerakkan badan untuk menghindari rintangan merah     |
| **Ambil Power-up**   | Sentuh power-up kuning dengan tangan terbuka         |
| **Menu Navigation**  | Arahkan tangan ke tombol dan tahan                   |

### 🎯 Game Objects

- **🟢 Green Targets**: +10 poin - Pukul untuk skor
- **🔴 Red Obstacles**: -1 nyawa - Hindari atau game over!
- **🟡 Yellow Power-ups**: Bonus special:
  - 🛡️ **Shield**: Imunitas sementara dari obstacle
  - ⭐ **Double Score**: Skor ganda selama durasi tertentu
  - 🐌 **Slow Motion**: Perlambat pergerakan objek

### ⌨️ Keyboard Shortcuts

| Key   | Fungsi                   |
| ----- | ------------------------ |
| `ESC` | Kembali ke menu utama    |
| `M`   | Toggle background music  |
| `S`   | Toggle sound effects     |
| `+/-` | Adjust volume            |
| `Q`   | Quit game                |
| `R`   | Restart (saat game over) |

---

## 📂 Struktur Project

```
Mulmed-Ceria/
├── 📄 main.py                 # Entry point (State Pattern)
├── ⚙️ config.py               # Game constants & settings
├── 🎮 game_engine.py          # Core game logic
│
├── 🧠 core/                   # Core systems
│   └── game_state_manager.py  # State management
│
├── 🎭 states/                 # Game states
│   ├── base_state.py          # Abstract base class
│   ├── menu_state.py          # Main menu
│   ├── countdown_state.py     # Pre-game countdown
│   ├── gameplay_state.py      # Main gameplay
│   ├── game_over_state.py     # Game over screen
│   ├── credits_state.py       # Credits
│   └── guide_state.py         # Tutorial
│
├── 🎨 rendering/              # Rendering components
│   ├── renderer.py            # Main renderer
│   ├── ui_renderer.py         # UI elements
│   ├── stickman_renderer.py   # Pose visualization
│   └── countdown_renderer.py  # Countdown animation
│
├── 🕵️ detection/              # AI/ML components
│   ├── pose_detector.py       # MediaPipe pose tracking
│   └── collision_detector.py  # Collision system
│
├── 👔 managers/               # Game managers
│   ├── camera_manager.py      # Webcam handling
│   ├── menu_manager.py        # Menu system
│   ├── sound_manager.py       # Audio system
│   ├── score_manager.py       # Scoring & lives
│   └── spawn_manager.py       # Object spawning
│
├── 🎯 entities/               # Game objects
│   └── game_objects.py        # Target, Obstacle, PowerUp
│
├── 🛠️ utils/                  # Utilities
│   └── helpers.py             # Helper functions
│
└── 📁 assets/                 # Game assets
    ├── images/                # Sprites & UI
    └── sounds/                # Audio files
```

---

## 🛠️ Tech Stack

| Technology                                                                                         | Purpose                    |
| -------------------------------------------------------------------------------------------------- | -------------------------- |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)       | Core programming language  |
| ![MediaPipe](https://img.shields.io/badge/MediaPipe-00897B?style=flat&logo=google&logoColor=white) | Pose & hand detection      |
| ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)       | Image processing & camera  |
| ![Pygame](https://img.shields.io/badge/Pygame-00A300?style=flat&logo=python&logoColor=white)       | Game framework & rendering |
| ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)          | Numerical computations     |

---

## 📝 Dependencies

```
opencv-python>=4.8.0
mediapipe>=0.10.0
pygame>=2.5.0
numpy>=1.24.0
```

---

## 🤝 Contributing

Contributions are welcome! Untuk contribute:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

---

## 🙏 Acknowledgments

- **MediaPipe** team untuk pose detection framework
- **Pygame** community untuk game development tools
- **OpenCV** contributors untuk computer vision library
- Semua yang telah memberikan feedback dan support

---

<div align="center">

### 🌟 Jangan lupa berikan ⭐ jika project ini membantu!

**Made with ❤️ by Cam-Fu Team**

[⬆ Back to Top](#-cam-fu)

</div>
