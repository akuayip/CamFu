"""
Game Renderer Module
Handles all drawing operations for the Cam-Fu game.
"""

import pygame
import mediapipe as mp
import os

class GameRenderer:
    """
    Handles all rendering tasks, including UI, stickman, hands, and objects.
    """

    def __init__(self, screen, assets_dir='assets/images'):
        """
        Initialize the renderer.
        Args:
            screen: The main pygame.Surface to draw on.
            assets_dir: Directory containing image assets
        """
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.assets_dir = assets_dir
        
        # Colors 
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 150, 255)
        self.ORANGE = (255, 165, 0)
        self.CYAN = (0, 255, 255)
        self.PURPLE = (200, 0, 255)
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 20)
        
        # Load blood image for lives
        self.blood_image = None
        blood_path = os.path.join(self.assets_dir, 'blood.png')
        if os.path.exists(blood_path):
            self.blood_image = pygame.image.load(blood_path).convert_alpha()
            self.blood_image = pygame.transform.smoothscale(self.blood_image, (50, 50))
        else:
            print(f"[Warning] Blood image not found: {blood_path}")
        
        # Load gameplay background
        self.play_bg = None
        play_bg_path = os.path.join(self.assets_dir, 'main_page.png')
        if os.path.exists(play_bg_path):
            self.play_bg = pygame.image.load(play_bg_path).convert()
            self.play_bg = pygame.transform.scale(self.play_bg, (self.screen_width, self.screen_height))
        else:
            print(f"[Warning] Gameplay background not found: {play_bg_path}")
        
        # --- ASET GAME OVER ---
        # 1. Gambar Game Over
        self.game_over_image = None
        game_over_path = os.path.join(self.assets_dir, 'game_over.png')
        if os.path.exists(game_over_path):
            self.game_over_image = pygame.image.load(game_over_path).convert_alpha()
        else:
            print(f"[Warning] Game over image not found: {game_over_path}")
        
        # 2. Background Landing Page
        self.landing_page_bg = None
        landing_path = os.path.join(self.assets_dir, 'landing_page.png')
        if os.path.exists(landing_path):
            self.landing_page_bg = pygame.image.load(landing_path).convert()
            self.landing_page_bg = pygame.transform.scale(self.landing_page_bg, (self.screen_width, self.screen_height))
        else:
            print(f"[Warning] Landing page background not found: {landing_path}")
        
        # 3. Tombol Menu
        self.menu_button = None
        menu_path = os.path.join(self.assets_dir, 'menu.png')
        if os.path.exists(menu_path):
            self.menu_button = pygame.image.load(menu_path).convert_alpha()
            self.menu_button = pygame.transform.smoothscale(self.menu_button, (80, 80))
        else:
            print(f"[Warning] Menu button not found: {menu_path}")
        
        # MediaPipe pose landmarks
        self.mp_pose = mp.solutions.pose.PoseLandmark
        
        self.game_over_played = False

    def update_screen_size(self, new_w, new_h):
        """Update screen dimensions when resized."""
        self.screen_width = new_w
        self.screen_height = new_h
        
        # Rescale background if exists
        if self.play_bg:
            play_bg_path = os.path.join(self.assets_dir, 'play_bg.png')
            if os.path.exists(play_bg_path):
                self.play_bg = pygame.image.load(play_bg_path).convert()
                self.play_bg = pygame.transform.scale(self.play_bg, (new_w, new_h))
        
        # Rescale landing page if exists
        if self.landing_page_bg:
            landing_path = os.path.join(self.assets_dir, 'landing_page.png')
            if os.path.exists(landing_path):
                self.landing_page_bg = pygame.image.load(landing_path).convert()
                self.landing_page_bg = pygame.transform.scale(self.landing_page_bg, (new_w, new_h))

    def clear_screen(self):
        """Fills the screen with background or black."""
        if self.play_bg:
            self.screen.blit(self.play_bg, (0, 0))
        else:
            self.screen.fill(self.BLACK)

    def draw_game_objects(self, targets, obstacles, powerups):
        """Draw all active game objects."""
        for target in targets:
            target.draw(self.screen)
            
        for obstacle in obstacles:
            obstacle.draw(self.screen)
            
        for powerup in powerups:
            powerup.draw(self.screen)

    def draw_hand_indicators(self, hand_info):
        """
        Draw visual indicators for hands and fist status.
        Args:
            hand_info: Dictionary containing left_hand and right_hand info
        """
        # Draw left hand indicator
        if hand_info['left_hand']['position']:
            pos = hand_info['left_hand']['position']
            is_fist = hand_info['left_hand']['is_fist']
            
            # Draw circle around hand
            color = self.RED if is_fist else self.CYAN
            pygame.draw.circle(self.screen, color, pos, 35, 3)
            
            # Draw fist icon/indicator
            if is_fist:
                # Draw filled circle for fist
                pygame.draw.circle(self.screen, self.RED, pos, 20)
                # Draw "FIST" text above
                fist_text = self.font_tiny.render("FIST", True, self.RED)
                self.screen.blit(fist_text, (pos[0] - 20, pos[1] - 50))
        
        # Draw right hand indicator
        if hand_info['right_hand']['position']:
            pos = hand_info['right_hand']['position']
            is_fist = hand_info['right_hand']['is_fist']
            
            # Draw circle around hand
            color = self.RED if is_fist else self.CYAN
            pygame.draw.circle(self.screen, color, pos, 35, 3)
            
            # Draw fist icon/indicator
            if is_fist:
                # Draw filled circle for fist
                pygame.draw.circle(self.screen, self.RED, pos, 20)
                # Draw "FIST" text above
                fist_text = self.font_tiny.render("FIST", True, self.RED)
                self.screen.blit(fist_text, (pos[0] - 20, pos[1] - 50))

    def draw_ui(self, score_manager, clock, hand_info):
        """
        Draw UI elements (score, lives, hand status, etc.).
        """
        # === BLOOD/LIVES (TOP LEFT CORNER) ===
        blood_size = 50  # Ukuran blood (50x50 px)
        blood_spacing = 10  # Jarak antar blood
        blood_start_x = 20  # 20px dari kiri
        blood_start_y = 20  # 20px dari atas
        
        for i in range(score_manager.lives):
            x = blood_start_x + i * (blood_size + blood_spacing)
            y = blood_start_y
            
            if self.blood_image:
                self.screen.blit(self.blood_image, (x, y))
            else:
                # Fallback: red circles if image not found
                pygame.draw.circle(self.screen, self.RED, (x + blood_size//2, y + blood_size//2), blood_size//2)
        
        # === SCORE (TOP RIGHT CORNER) ===
        score_text = self.font_medium.render(f"SCORE: {score_manager.score}", True, self.WHITE)
        score_x = self.screen_width - score_text.get_width() - 20
        self.screen.blit(score_text, (score_x, 20))
        
        # === FPS (BOTTOM RIGHT CORNER) ===
        fps = int(clock.get_fps())
        fps_text = self.font_small.render(f"FPS: {fps}", True, self.GREEN)
        fps_x = self.screen_width - fps_text.get_width() - 20
        fps_y = self.screen_height - fps_text.get_height() - 20
        self.screen.blit(fps_text, (fps_x, fps_y))

        # === ACTIVE POWER-UPS (BELOW BLOOD - TOP LEFT) ===
        y_offset = blood_start_y + blood_size + 15  # Start below blood icons
        if score_manager.shield_active:
            shield_text = self.font_small.render(
                f"SHIELD: {int(score_manager.shield_duration)}s", True, self.BLUE
            )
            self.screen.blit(shield_text, (20, y_offset))
            y_offset += 30

        if score_manager.double_score_active:
            double_text = self.font_small.render(
                f"2X SCORE: {int(score_manager.double_score_duration)}s", True, self.YELLOW
            )
            self.screen.blit(double_text, (20, y_offset))
            y_offset += 30

        if score_manager.slow_motion_active:
            slow_text = self.font_small.render(
                f"SLOW-MO: {int(score_manager.slow_motion_duration)}s", True, self.GREEN
            )
            self.screen.blit(slow_text, (20, y_offset))
            y_offset += 30

        # === HAND STATUS (BOTTOM LEFT CORNER) ===
        hand_status_y = self.screen_height - 90  # Adjusted for corner positioning
        
        # Title
        status_title = self.font_small.render("HAND STATUS:", True, self.WHITE)
        self.screen.blit(status_title, (20, hand_status_y))
        
        # Left hand status
        left_status = " FIST" if hand_info['left_hand']['is_fist'] else " OPEN"
        left_color = self.RED if hand_info['left_hand']['is_fist'] else self.CYAN
        left_detected = hand_info['left_hand']['position'] is not None
        
        if left_detected:
            left_text = self.font_small.render(f"LEFT: {left_status}", True, left_color)
        else:
            left_text = self.font_small.render("LEFT: ---", True, (100, 100, 100))
        self.screen.blit(left_text, (20, hand_status_y + 30))
        
        # Right hand status
        right_status = " FIST" if hand_info['right_hand']['is_fist'] else " OPEN"
        right_color = self.RED if hand_info['right_hand']['is_fist'] else self.CYAN
        right_detected = hand_info['right_hand']['position'] is not None
        
        if right_detected:
            right_text = self.font_small.render(f"RIGHT: {right_status}", True, right_color)
        else:
            right_text = self.font_small.render("RIGHT: ---", True, (100, 100, 100))
        self.screen.blit(right_text, (20, hand_status_y + 55))

        # === INSTRUCTIONS (BOTTOM CENTER) ===
        inst_text = self.font_tiny.render(
            "PUNCH targets with FIST  | DODGE obstacles (red) | GRAB powerups (yellow)",
            True, self.WHITE
        )
        inst_x = self.screen_width // 2 - inst_text.get_width() // 2
        inst_y = self.screen_height - 25
        self.screen.blit(inst_text, (inst_x, inst_y))

    def draw_game_over_screen(self, score_manager, play_duration=0, phase=1):
        """
        Draws the Game Over screen with sequential animation.
        Phase 1: Black Screen + Game Over Logo (Intro)
        Phase 2: Landing BG + Score + Time + Menu Button
        """
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        if phase == 1:
            # === FASE 1: LAYAR HITAM + LOGO GAME OVER ===
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.set_alpha(150) 
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))

            # Gambar Logo Game Over di tengah
            if self.game_over_image:
                img_width = int(self.screen_width * 0.5)
                img_height = int(self.screen_height * 0.4)
                scaled_img = pygame.transform.scale(self.game_over_image, (img_width, img_height))
                img_x = (self.screen_width - img_width) // 2
                img_y = (self.screen_height - img_height) // 2
                self.screen.blit(scaled_img, (img_x, img_y))
            else:
                # Fallback teks jika gambar tidak ada
                text = self.font_large.render("GAME OVER", True, self.RED)
                text_rect = text.get_rect(center=(center_x, center_y))
                self.screen.blit(text, text_rect)

        elif phase == 2:
            # === FASE 2: HASIL AKHIR (Background + Skor) ===
            # 1. Background Landing Page
            if self.landing_page_bg:
                self.screen.blit(self.landing_page_bg, (0, 0))
            else:
                self.screen.fill(self.BLACK)

            # 2. Hitung Waktu (Menit:Detik)
            minutes = int(play_duration) // 60
            seconds = int(play_duration) % 60
            time_str = f"{minutes:02d}:{seconds:02d}"

            # 3. Tampilkan Skor dan Waktu
            score_text = self.font_medium.render(f"FINAL SCORE: {score_manager.score}", True, self.WHITE)
            time_text = self.font_medium.render(f"TIME PLAYED: {time_str}", True, self.YELLOW)
            
            score_rect = score_text.get_rect(center=(center_x, center_y + 35))
            time_rect = time_text.get_rect(center=(center_x, center_y + 75))
            
            self.screen.blit(score_text, score_rect)
            self.screen.blit(time_text, time_rect)

            # 5. Tombol Menu (Pojok Kiri Bawah)
            if self.menu_button:
                self.screen.blit(self.menu_button, (30, self.screen_height - 130))
            

    def draw_stickman(self, landmarks, pose_detector):
        """
        Draw stickman overlay on game screen.
        (KEMBALI KE KODE ORIGINAL PANJANG)
        """
        if not landmarks:
            return

        BODY_COLOR = self.WHITE 
        LINE_THICKNESS = 65       
        JOINT_RADIUS = LINE_THICKNESS // 2

        # Get landmarks explicitly
        nose = pose_detector.get_landmark_position(landmarks, self.mp_pose.NOSE.value, self.screen_width, self.screen_height)
        left_ear = pose_detector.get_landmark_position(landmarks, self.mp_pose.LEFT_EAR.value, self.screen_width, self.screen_height)
        right_ear = pose_detector.get_landmark_position(landmarks, self.mp_pose.RIGHT_EAR.value, self.screen_width, self.screen_height)
        
        left_shoulder = pose_detector.get_landmark_position(landmarks, self.mp_pose.LEFT_SHOULDER.value, self.screen_width, self.screen_height)
        right_shoulder = pose_detector.get_landmark_position(landmarks, self.mp_pose.RIGHT_SHOULDER.value, self.screen_width, self.screen_height)
        left_hip = pose_detector.get_landmark_position(landmarks, self.mp_pose.LEFT_HIP.value, self.screen_width, self.screen_height)
        right_hip = pose_detector.get_landmark_position(landmarks, self.mp_pose.RIGHT_HIP.value, self.screen_width, self.screen_height)
        
        left_elbow = pose_detector.get_landmark_position(landmarks, self.mp_pose.LEFT_ELBOW.value, self.screen_width, self.screen_height)
        left_wrist = pose_detector.get_landmark_position(landmarks, self.mp_pose.LEFT_WRIST.value, self.screen_width, self.screen_height)
        right_elbow = pose_detector.get_landmark_position(landmarks, self.mp_pose.RIGHT_ELBOW.value, self.screen_width, self.screen_height)
        right_wrist = pose_detector.get_landmark_position(landmarks, self.mp_pose.RIGHT_WRIST.value, self.screen_width, self.screen_height)
        
        left_knee = pose_detector.get_landmark_position(landmarks, self.mp_pose.LEFT_KNEE.value, self.screen_width, self.screen_height)
        left_ankle = pose_detector.get_landmark_position(landmarks, self.mp_pose.LEFT_ANKLE.value, self.screen_width, self.screen_height)
        right_knee = pose_detector.get_landmark_position(landmarks, self.mp_pose.RIGHT_KNEE.value, self.screen_width, self.screen_height)
        right_ankle = pose_detector.get_landmark_position(landmarks, self.mp_pose.RIGHT_ANKLE.value, self.screen_width, self.screen_height)
        
        neck_point = None
        pelvis_point = None

        if left_shoulder and right_shoulder:
            neck_point = (
                (left_shoulder[0] + right_shoulder[0]) // 2,
                (left_shoulder[1] + right_shoulder[1]) // 2
            )

        if left_hip and right_hip:
            pelvis_point = (
                (left_hip[0] + right_hip[0]) // 2,
                (left_hip[1] + right_hip[1]) // 2
            )

        head_center = None
        head_radius = 30 

        if nose:
            head_center_x_calc = nose[0]
            head_center_y_calc = nose[1] 
            
            if left_ear and right_ear:
                ear_distance = abs(left_ear[0] - right_ear[0])
                head_radius = int(ear_distance * 0.75)
            
            head_center_y_calc = nose[1] 
            head_center = (head_center_x_calc, head_center_y_calc)
            pygame.draw.circle(self.screen, BODY_COLOR, head_center, head_radius) 

        if neck_point and pelvis_point:
            pygame.draw.line(self.screen, BODY_COLOR, neck_point, pelvis_point, LINE_THICKNESS)
            
            if head_center:
                pygame.draw.line(self.screen, BODY_COLOR, head_center, neck_point, LINE_THICKNESS)

        if neck_point:
            if left_elbow:
                pygame.draw.line(self.screen, BODY_COLOR, neck_point, left_elbow, LINE_THICKNESS)
                if left_wrist:
                    pygame.draw.line(self.screen, BODY_COLOR, left_elbow, left_wrist, LINE_THICKNESS)
            
            if right_elbow:
                pygame.draw.line(self.screen, BODY_COLOR, neck_point, right_elbow, LINE_THICKNESS)
                if right_wrist:
                    pygame.draw.line(self.screen, BODY_COLOR, right_elbow, right_wrist, LINE_THICKNESS)

        if pelvis_point:
            if left_knee:
                pygame.draw.line(self.screen, BODY_COLOR, pelvis_point, left_knee, LINE_THICKNESS)
                if left_ankle:
                    pygame.draw.line(self.screen, BODY_COLOR, left_knee, left_ankle, LINE_THICKNESS)
            
            if right_knee:
                pygame.draw.line(self.screen, BODY_COLOR, pelvis_point, right_knee, LINE_THICKNESS)
                if right_ankle:
                    pygame.draw.line(self.screen, BODY_COLOR, right_knee, right_ankle, LINE_THICKNESS)
                            
        all_joints = [
            neck_point,    
            pelvis_point,   
            left_elbow,
            right_elbow,
            left_knee,
            right_knee,
            left_wrist,     
            right_wrist,
            left_ankle,     
            right_ankle
        ]

        for joint in all_joints:
            if joint:
                pygame.draw.circle(self.screen, BODY_COLOR, joint, JOINT_RADIUS)
        
        if head_center:
            pygame.draw.circle(self.screen, BODY_COLOR, head_center, head_radius)