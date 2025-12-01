import pygame
import sys
import os
import cv2
import mediapipe as mp
import time

from game_engine import GameEngine
from pose_detector import PoseDetector
from renderer import GameRenderer
from spawn_manager import SpawnManager
from menu_manager import MenuManager
from sound_manager import SoundManager

# Game States
GAME_MENU = 0
GAME_COUNTDOWN = 1
GAME_PLAY = 2
GAME_OVER = 3
GAME_CREDITS = 4
GAME_GUIDE = 5

pygame.init()
pygame.font.init()

def get_available_cameras():
    """Deteksi kamera yang tersedia di sistem."""
    available_cameras = []
    
    # Coba setiap kamera dari 0 hingga 10 (umumnya cukup untuk mengecek)
    for i in range(10):
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Test read capability
                ret, frame = cap.read()
                if ret:
                    available_cameras.append(i)
            cap.release()
        except Exception as e:
            continue
    
    return available_cameras

def is_same_position(pos1, pos2, threshold=80):
    if pos1 is None or pos2 is None:
        return False
    return abs(pos1[0] - pos2[0]) < threshold and abs(pos1[1] - pos2[1]) < threshold

def select_camera_terminal(available_cameras):
    """Menu pemilihan kamera via terminal."""
    print("\n" + "="*60)
    print("        PILIH KAMERA - CAM-FU")
    print("="*60)

    if not available_cameras:
        print("Error: Tidak ada kamera yang ditemukan!")
        return None

    print(f"\nKamera yang tersedia ({len(available_cameras)} kamera):")
    print("-" * 40)

    for i, cam_idx in enumerate(available_cameras, 1):
        print(f"{i}. Kamera {cam_idx}")

    print("\nKetik nomor kamera yang ingin digunakan (1-{}):".format(len(available_cameras)))
    print("Atau ketik 'q' untuk keluar")

    while True:
        try:
            choice = input("\nPilihan Anda: ").strip().lower()

            if choice == 'q':
                print("Pembatalan pemilihan kamera. Keluar dari aplikasi.")
                sys.exit(0)

            # Validasi input
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(available_cameras):
                    selected_camera = available_cameras[choice_idx]
                    print(f"\n✓ Kamera {selected_camera} telah dipilih!")
                    return selected_camera
                else:
                    print(f"❌ Nomor tidak valid. Pilih antara 1-{len(available_cameras)} atau 'q' untuk keluar")
            except ValueError:
                print("❌ Input tidak valid. Masukkan nomor atau 'q' untuk keluar")

        except KeyboardInterrupt:
            print("\n\nPembatalan pemilihan kamera. Keluar dari aplikasi.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}. Coba lagi.")

def main():
    SCREEN_W, SCREEN_H = 1280, 720
    FPS = 60
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.RESIZABLE)
    pygame.display.set_caption("Cam-Fu - Pose Fighting Game")
    clock = pygame.time.Clock()

    # Deteksi dan pilih kamera terlebih dahulu via terminal
    print("="*60)
    print("        CAM-FU - POSE FIGHTING GAME")
    print("="*60)
    print("\nMencari kamera yang tersedia...")
    
    available_cameras = get_available_cameras()
    
    if not available_cameras:
        print("Error: Tidak ada kamera yang ditemukan.")
        print("Pastikan kamera web telah terhubung dan tidak digunakan oleh aplikasi lain.")
        sys.exit()
    
    print(f"\n✓ Berhasil menemukan {len(available_cameras)} kamera: {available_cameras}")
    
    # Pilih kamera via terminal
    if len(available_cameras) == 1:
        selected_camera = available_cameras[0]
        print(f"\n✓ Menggunakan kamera {selected_camera} (hanya satu kamera tersedia)")
    else:
        selected_camera = select_camera_terminal(available_cameras)
        
        if selected_camera is None:
            print("Gagal memilih kamera. Keluar dari aplikasi.")
            sys.exit()

    # Initialize camera with selected device
    cap = cv2.VideoCapture(selected_camera)
    if not cap.isOpened():
        print(f"Error: Tidak dapat membuka kamera {selected_camera}.")
        sys.exit()

    # Asset Background Sendiri
    try:
        game_bg = pygame.image.load("assets/images/play_bg.jpg").convert()
    except FileNotFoundError:
        print("Warning: assets/images/play_bg.jpg tidak ditemukan.")
        game_bg = pygame.Surface((1280, 720)) 

    # Core modules
    pose_detector = PoseDetector()
    game_renderer = GameRenderer(screen, assets_dir='assets/images')
    spawn_manager = SpawnManager(SCREEN_W, SCREEN_H)
    
    game_engine = GameEngine(
        screen=screen,
        pose_detector=pose_detector,
        game_renderer=game_renderer,
        spawn_manager=spawn_manager
    )

    menu = MenuManager(screen, 'assets/images')
    
    # Sound manager
    sound_manager = SoundManager()
    
    # Connect sound manager to menu
    menu.sound_manager = sound_manager

    # Input states
    current_state = GAME_MENU
    
    # Countdown variables
    countdown_timer = 3.0
    countdown_images = {}
    
    # Load countdown images
    for i in [1, 2, 3]:
        img_path = f'assets/images/cd_{i}.png'
        if os.path.exists(img_path):
            img = pygame.image.load(img_path).convert_alpha()
            countdown_images[i] = pygame.transform.smoothscale(img, (200, 200))
        else:
            print(f"[Warning] Countdown image not found: {img_path}")
    
    # Start menu music
    sound_manager.play_music('menu', loops=-1, fade_ms=1000)

    # Anti-spam mechanism for fist clicks
    last_fist_time = 0
    FIST_COOLDOWN = 0.5  # 500ms cooldown between fist clicks

    # Variabel Waktu & Animasi
    start_time = 0
    play_duration = 0
    game_over_timer = 0.0  # Timer untuk animasi intro game over

    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        current_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds

        # Event Handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                
            elif e.type == pygame.VIDEORESIZE:
                SCREEN_W, SCREEN_H = e.w, e.h
                screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.RESIZABLE)
                if hasattr(game_renderer, 'update_screen_size'):
                    game_renderer.update_screen_size(SCREEN_W, SCREEN_H)
                spawn_manager.update_screen_size(SCREEN_W, SCREEN_H)
                
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    running = False
                
                # Kontrol Volume 
                elif e.key == pygame.K_m: 
                    sound_manager.toggle_music()
                elif e.key == pygame.K_s: 
                    sound_manager.toggle_sound()
                elif e.key == pygame.K_PLUS or e.key == pygame.K_EQUALS:
                    sound_manager.set_music_volume(sound_manager.music_volume + 0.1)
                elif e.key == pygame.K_MINUS:
                    sound_manager.set_music_volume(sound_manager.music_volume - 0.1)
                
                # Navigasi Menu
                elif e.key == pygame.K_ESCAPE:
                    if current_state in (GAME_CREDITS, GAME_GUIDE, GAME_COUNTDOWN, GAME_PLAY):
                        current_state = GAME_MENU
                        sound_manager.crossfade_music('menu', fade_out_ms=500, fade_in_ms=500)
                        
                # Restart manual (hanya aktif setelah animasi intro selesai)
                elif current_state == GAME_OVER and game_over_timer > 2.5 and e.key == pygame.K_r:
                    current_state = GAME_COUNTDOWN
                    countdown_timer = 3.0
                    game_engine.reset_game()
                    sound_manager.stop_music()
                    sound_manager.play_sound('countdown')

        # Read Camera
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        cam_h, cam_w = frame.shape[:2]
        _, landmarks = pose_detector.detect_pose(frame)

        # Hand Tracking / Cursor System
        active_hand_pos = None
        right_idx_pos = None
        left_idx_pos = None

        if landmarks:
            scale_x = SCREEN_W / 1280
            scale_y = SCREEN_H / 720

            raw_right = pose_detector.get_landmark_position(
                landmarks, mp.solutions.pose.PoseLandmark.RIGHT_INDEX.value, cam_w, cam_h)
            raw_left = pose_detector.get_landmark_position(
                landmarks, mp.solutions.pose.PoseLandmark.LEFT_INDEX.value, cam_w, cam_h)

            if raw_right:
                right_idx_pos = pose_detector.to_screen_coordinates(
                    raw_right[0] * scale_x, raw_right[1] * scale_y, 
                    cam_w, cam_h, SCREEN_W, SCREEN_H)
            if raw_left:
                left_idx_pos = pose_detector.to_screen_coordinates(
                    raw_left[0] * scale_x, raw_left[1] * scale_y, 
                    cam_w, cam_h, SCREEN_W, SCREEN_H)

            # Check hover (for cursor display only)
            hover_right = menu.check_button_hover(right_idx_pos) if current_state != GAME_PLAY else None
            hover_left = menu.check_button_hover(left_idx_pos) if current_state != GAME_PLAY else None

            if hover_right: 
                active_hand_pos = right_idx_pos
            elif hover_left: 
                active_hand_pos = left_idx_pos
            elif right_idx_pos: 
                active_hand_pos = right_idx_pos
            elif left_idx_pos: 
                active_hand_pos = left_idx_pos

        # Background Rendering
        if current_state in (GAME_PLAY, GAME_COUNTDOWN):
            bg_scaled = pygame.transform.scale(game_bg, (SCREEN_W, SCREEN_H))
            screen.blit(bg_scaled, (0, 0))
        elif current_state != GAME_OVER:
            # Menu/Guide/Credits pakai kamera
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_py = pygame.image.frombuffer(
                frame_rgb.tobytes(), frame.shape[1::-1], "RGB")
            frame_py = pygame.transform.scale(frame_py, (SCREEN_W, SCREEN_H))
            screen.blit(frame_py, (0, 0))

        # Game State Machine
        if current_state == GAME_MENU:
            # Ensure menu music is playing
            if sound_manager.current_music != 'menu':
                sound_manager.crossfade_music('menu', fade_out_ms=500, fade_in_ms=500)

            menu.draw_menu()

            # Get hand info for fist detection
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand_info = pose_detector.get_hand_info(frame_rgb, SCREEN_W, SCREEN_H)

            # Check for fist click on buttons (with cooldown)
            fist_button = menu.check_button_fist_click(hand_info)
            if fist_button and (current_time - last_fist_time) > FIST_COOLDOWN:
                last_fist_time = current_time
                menu.play_button_sound()
                if fist_button == "start":
                    current_state = GAME_COUNTDOWN
                    countdown_timer = 3.0
                    game_engine.reset_game()
                    sound_manager.stop_music()
                    sound_manager.play_sound('countdown')
                elif fist_button == "credits":
                    current_state = GAME_CREDITS
                elif fist_button == "guide":
                    current_state = GAME_GUIDE

        elif current_state == GAME_COUNTDOWN:
            dark_overlay = pygame.Surface((SCREEN_W, SCREEN_H))
            dark_overlay.set_alpha(180)
            dark_overlay.fill((0, 0, 0))
            screen.blit(dark_overlay, (0, 0))
            
            countdown_timer -= dt
            
            if countdown_timer > 2.0: 
                num = 3
            elif countdown_timer > 1.0: 
                num = 2
            elif countdown_timer > 0.0: 
                num = 1
            else:
                current_state = GAME_PLAY
                sound_manager.play_music('gameplay')
                # RESET Timer
                start_time = time.time()
                game_over_timer = 0.0 
                continue
            
            if num in countdown_images:
                img = countdown_images[num]
                img_rect = img.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
                screen.blit(img, img_rect)
            else:
                font_cd = pygame.font.Font(None, 200)
                text = font_cd.render(str(num), True, (255, 255, 255))
                text_rect = text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
                screen.blit(text, text_rect)

        elif current_state == GAME_PLAY:
            # Hitung waktu main
            play_duration = time.time() - start_time

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand_info = pose_detector.get_hand_info(frame_rgb, SCREEN_W, SCREEN_H)
            
            game_engine.update(dt, landmarks, hand_info)

            # Background already drawn above in "Background Rendering" section
            
            game_renderer.draw_game_objects(
                game_engine.targets,
                game_engine.obstacles,
                game_engine.powerups)
            
            if landmarks:
                game_renderer.draw_stickman(landmarks, pose_detector)
            
            game_renderer.draw_hand_indicators(hand_info)
            game_renderer.draw_ui(game_engine.score_manager, clock, hand_info)
            
            if game_engine.score_manager.game_over:
                current_state = GAME_OVER
                sound_manager.stop_music()
                game_over_timer = 0.0 

        elif current_state == GAME_CREDITS:
            menu.draw_credits_screen()
            
            # Get hand info for fist detection
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand_info = pose_detector.get_hand_info(frame_rgb, SCREEN_W, SCREEN_H)
            
            # Check for fist click on back button (with cooldown)
            fist_button = menu.check_button_fist_click(hand_info)
            if fist_button == "back" and (current_time - last_fist_time) > FIST_COOLDOWN:
                menu.play_button_sound()
                last_fist_time = current_time
                current_state = GAME_MENU

        elif current_state == GAME_GUIDE:
            menu.draw_guide_screen()
            
            # Get hand info for fist detection
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand_info = pose_detector.get_hand_info(frame_rgb, SCREEN_W, SCREEN_H)
            
            # Check for fist click on back button (with cooldown)
            fist_button = menu.check_button_fist_click(hand_info)
            if fist_button == "back" and (current_time - last_fist_time) > FIST_COOLDOWN:
                menu.play_button_sound()
                last_fist_time = current_time
                current_state = GAME_MENU

        elif current_state == GAME_OVER:
            # Tambah timer
            game_over_timer += dt
            
            # PHASE 1: 0 - 2.5 Detik (Intro Hitam)
            if game_over_timer < 2.5:
                black_screen = pygame.Surface((SCREEN_W, SCREEN_H))
                black_screen.fill((0, 0, 0))
                screen.blit(black_screen, (0, 0))
            
            # PHASE 2: Setelah 2.5 Detik (Game Over Screen)
            else:
                # Draw game elements with game over overlay
                game_renderer.draw_game_objects(
                    game_engine.targets, game_engine.obstacles, game_engine.powerups)
                
                if landmarks:
                    game_renderer.draw_stickman(landmarks, pose_detector)
                
                # hand_info untuk game over screen (kosong jika tidak ada)
                empty_hand_info = {
                    'left_hand': {'position': None, 'is_fist': False},
                    'right_hand': {'position': None, 'is_fist': False}
                }
                game_renderer.draw_ui(game_engine.score_manager, clock, empty_hand_info)

        # Cursor Rendering (Hidden During Gameplay)
        if current_state != GAME_PLAY:
            if right_idx_pos:
                pygame.draw.circle(screen, (150, 150, 150), right_idx_pos, 10, 2)
            if left_idx_pos:
                pygame.draw.circle(screen, (150, 150, 150), left_idx_pos, 10, 2)

            if active_hand_pos:
                pygame.draw.circle(screen, (0, 255, 255), active_hand_pos, 20, 3)

        pygame.display.flip()

    cap.release()
    sound_manager.cleanup()
    game_engine.cleanup()
    sys.exit()


if __name__ == "__main__":
    main()