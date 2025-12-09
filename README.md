# Cam-Fu

## Deskripsi Project

Cam-Fu adalah game interaktif berbasis webcam yang menjadikan pemain sebagai petarung kungfu digital. Pemain meninju ikon-ikon melayang di layar untuk mendapatkan poin, namun harus menghindari jebakan berupa sarung tinju melayang yang akan menyerang balik dan mengurangi skor. Game ini menggunakan deteksi gerakan tangan real-time untuk mengontrol aksi di layar. Visual berupa stickman dan efek suara kungfu, layaknya game VR hanya dengan webcam.

## Anggota Kelompok

| Nama Lengkap          | NIM       | GitHub ID                                           |
| --------------------- | --------- | --------------------------------------------------- |
| Cindy Nadila Putri    | 122140002 | [cindynadilaptr](https://github.com/cindynadilaptr) |
| M. Arief Rahman Hakim | 122140083 | [akuayip](https://github.com/akuayip)               |
| Zidan Raihan          | 122140100 | [zidbytes](https://github.com/zidbytes)             |

## Logbook Mingguan

| Minggu | Tanggal              | Progress/Update                                                                                                     |
| ------ | -------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 1      | 28 Okt - 2 Nov 2025  | - Membuat repository GitHub<br>- Diskusi ide project game berbasis webcam                                           |
| 2      | 4 Nov - 9 Nov 2025   | - Menambahkan asset untuk game<br>- Refactor sistem collision detection<br>- Implementasi body landmark to stickman |
| 3      | 11 Nov - 16 Nov 2025 | - Implementasi main menu                                                                                            |
| 4      | 18 Nov - 23 Nov 2025 | - Refactor collision detection pada kepala<br>- Implementasi hand landmark untuk deteksi buka/tutup tangan          |
| 5      | 25 Nov - 30 Nov 2025 |                                                                                                                     |

> Catatan: Silakan isi logbook setiap minggu sesuai perkembangan project.

## Instruksi Instalasi dan Penggunaan

### Prasyarat

- Python 3.10 atau 3.11 (MediaPipe tidak support Python 3.12+)
- Webcam (built-in atau external)
- Git

### 1. Clone Repository

```bash
git clone https://github.com/akuayip/CamFu.git
cd CamFu
```

### 2. Setup Python Environment

Pilih salah satu metode berikut:

#### **Metode A: Menggunakan Anaconda (Recommended)**

```bash
# Buat environment baru dengan Python 3.10
conda create -n camfu python=3.10 -y

# Aktifkan environment
conda activate camfu

# Install dependencies
pip install -r requirements.txt
```

#### **Metode B: Menggunakan UV (Fast Python Package Manager)**

```bash
# Install uv menggunakan pip jika belum
pip install uv

# Buat virtual environment dengan uv
uv venv --python 3.10

# Aktifkan environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# Install dependencies dengan uv (lebih cepat)
uv pip install -r requirements.txt
```

### 3. Menjalankan Program

```bash
python main.py
```
