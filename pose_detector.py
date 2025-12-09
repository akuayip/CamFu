"""
Pose Detector Module
Handles human pose detection and hand gesture recognition using MediaPipe.
"""

import mediapipe as mp
import cv2


class PoseDetector:
    """
    A class to detect human pose and hand gestures using MediaPipe.
    Detects body pose (33 landmarks) and hand gestures (21 landmarks per hand).
    """

    def __init__(
        self,
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ):
        """
        Initialize the PoseDetector with both pose and hands detection.

        Args:
            static_image_mode: Whether to treat input as static images
            model_complexity: Complexity of pose model (0, 1, or 2)
            smooth_landmarks: Whether to smooth landmarks across frames
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            smooth_landmarks=smooth_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Hand landmark indices for fist detection
        self.WRIST = 0
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8
        self.MIDDLE_TIP = 12
        self.RING_TIP = 16
        self.PINKY_TIP = 20

    def detect_pose(self, frame):
        """
        Detect pose landmarks in the given frame.

        Args:
            frame: Input BGR image from camera

        Returns:
            tuple: (processed_frame, landmarks)
                - processed_frame: RGB frame after processing
                - landmarks: Detected pose landmarks or None
        """
        # Convert BGR to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(frame_rgb)
        
        return frame_rgb, results.pose_landmarks

    def detect_hands(self, frame_rgb):
        """
        Detect hand landmarks in the given frame.

        Args:
            frame_rgb: Input RGB image

        Returns:
            hands_results: MediaPipe hands results containing multi_hand_landmarks and multi_handedness
        """
        results = self.hands.process(frame_rgb)
        return results

    def is_fist(self, hand_landmarks):
        """
        Determine if a hand is making a fist gesture.
        
        Algorithm:
        - Calculate distance from each fingertip to wrist
        - Calculate distance from each fingertip to palm center (landmark 0)
        - If all fingers are close to palm → FIST
        - If fingers are extended → OPEN HAND
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            bool: True if hand is making a fist, False otherwise
        """
        if not hand_landmarks:
            return False
        
        # Get wrist position
        wrist = hand_landmarks.landmark[self.WRIST]
        
        # Get fingertips
        thumb_tip = hand_landmarks.landmark[self.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.INDEX_TIP]
        middle_tip = hand_landmarks.landmark[self.MIDDLE_TIP]
        ring_tip = hand_landmarks.landmark[self.RING_TIP]
        pinky_tip = hand_landmarks.landmark[self.PINKY_TIP]
        
        # Calculate distances from fingertips to wrist (normalized 0-1)
        def distance(p1, p2):
            return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)**0.5
        
        # Threshold for fist detection
        # If fingertips are close to wrist, it's a fist
        FIST_THRESHOLD = 0.15  # Adjusted threshold
        
        index_dist = distance(index_tip, wrist)
        middle_dist = distance(middle_tip, wrist)
        ring_dist = distance(ring_tip, wrist)
        pinky_dist = distance(pinky_tip, wrist)
        
        # Check if all fingers (except thumb) are close to wrist
        fingers_closed = (
            index_dist < FIST_THRESHOLD and
            middle_dist < FIST_THRESHOLD and
            ring_dist < FIST_THRESHOLD and
            pinky_dist < FIST_THRESHOLD
        )
        
        return fingers_closed

    def get_hand_info(self, frame_rgb, frame_width, frame_height):
        """
        Get hand positions and fist status for both hands.
        
        Args:
            frame_rgb: RGB frame
            frame_width: Width of the frame in pixels
            frame_height: Height of the frame in pixels
            
        Returns:
            dict: {
                'left_hand': {
                    'position': (x, y) or None,
                    'is_fist': bool,
                    'landmarks': hand_landmarks or None
                },
                'right_hand': {
                    'position': (x, y) or None,
                    'is_fist': bool,
                    'landmarks': hand_landmarks or None
                }
            }
        """
        hands_results = self.detect_hands(frame_rgb)
        
        hand_info = {
            'left_hand': {'position': None, 'is_fist': False, 'landmarks': None},
            'right_hand': {'position': None, 'is_fist': False, 'landmarks': None}
        }
        
        if not hands_results.multi_hand_landmarks:
            return hand_info
        
        # Process each detected hand
        for idx, hand_landmarks in enumerate(hands_results.multi_hand_landmarks):
            # Determine if it's left or right hand
            handedness = hands_results.multi_handedness[idx].classification[0].label
            
            # Karena frame di-mirror di game_engine (cv2.flip), 
            # MediaPipe "Left" = tangan kiri user (tidak perlu swap)
            # MediaPipe "Right" = tangan kanan user (tidak perlu swap)
            hand_type = 'left_hand' if handedness == 'Left' else 'right_hand'
            
            # Get wrist position (landmark 0) as hand position
            wrist = hand_landmarks.landmark[self.WRIST]
            hand_position = (
                int(wrist.x * frame_width),
                int(wrist.y * frame_height)
            )
            
            # Detect fist gesture
            fist_detected = self.is_fist(hand_landmarks)
            
            # Store hand info
            hand_info[hand_type] = {
                'position': hand_position,
                'is_fist': fist_detected,
                'landmarks': hand_landmarks
            }
        
        return hand_info

    def get_landmark_position(self, landmarks, landmark_id, frame_width, frame_height):
        """
        Get the pixel position of a specific landmark.

        Args:
            landmarks: Pose landmarks object
            landmark_id: ID of the landmark to retrieve
            frame_width: Width of the frame
            frame_height: Height of the frame

        Returns:
            tuple: (x, y) pixel coordinates or None
        """
        if landmarks and len(landmarks.landmark) > landmark_id:
            landmark = landmarks.landmark[landmark_id]
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            return (x, y)
        return None
    
    def to_screen_coordinates(self, x, y, cam_w, cam_h, screen_w, screen_h):
        """Convert posisi landmark dari ukuran kamera → layar pygame."""
        sx = int((x / cam_w) * screen_w)
        sy = int((y / cam_h) * screen_h)
        return (sx, sy)

    def close(self):
        """Release resources."""
        self.pose.close()
        self.hands.close()
