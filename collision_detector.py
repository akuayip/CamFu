"""
Collision Detector Module
Handles collision detection between pose landmarks and game objects.
"""

import math
from typing import Tuple, Optional


class CollisionDetector:
    """
    Detects collisions between body parts (hands, body) and game objects.
    Supports fist gesture detection for punch validation.
    """

    def __init__(self, collision_radius=30):
        """
        Initialize CollisionDetector.

        Args:
            collision_radius: Radius for collision detection in pixels
        """
        self.collision_radius = collision_radius

    def point_distance(self, point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
        """
        Calculate Euclidean distance between two points.

        Args:
            point1: (x, y) coordinates of first point
            point2: (x, y) coordinates of second point

        Returns:
            float: Distance between points
        """
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def check_collision(
        self,
        landmark_pos: Optional[Tuple[int, int]],
        object_pos: Tuple[int, int],
        object_radius: int
    ) -> bool:
        """
        Check if a landmark collides with an object.

        Args:
            landmark_pos: (x, y) position of landmark (can be None)
            object_pos: (x, y) position of object center
            object_radius: Radius of the object

        Returns:
            bool: True if collision detected, False otherwise
        """
        if landmark_pos is None:
            return False

        distance = self.point_distance(landmark_pos, object_pos)
        return distance < (self.collision_radius + object_radius)

    def check_hand_collision(
        self,
        left_hand_pos: Optional[Tuple[int, int]],
        right_hand_pos: Optional[Tuple[int, int]],
        left_is_fist: bool,
        right_is_fist: bool,
        object_pos: Tuple[int, int],
        object_radius: int,
        require_fist: bool = False
    ) -> str:
        """
        Check if any hand collides with an object.

        Args:
            left_hand_pos: Position of left hand (wrist/palm center)
            right_hand_pos: Position of right hand (wrist/palm center)
            left_is_fist: Whether left hand is making a fist
            right_is_fist: Whether right hand is making a fist
            object_pos: Object center position
            object_radius: Object radius
            require_fist: If True, collision only valid when hand is fist (for punching targets)
                         If False, any hand contact is valid (for grabbing powerups)

        Returns:
            str: 'left', 'right', or '' (no collision)
        """
        # Check left hand
        if left_hand_pos is not None:
            if self.check_collision(left_hand_pos, object_pos, object_radius):
                # If fist is required, check fist status
                if require_fist:
                    if left_is_fist:
                        return 'left'
                else:
                    # No fist required (e.g., for powerups)
                    return 'left'

        # Check right hand
        if right_hand_pos is not None:
            if self.check_collision(right_hand_pos, object_pos, object_radius):
                # If fist is required, check fist status
                if require_fist:
                    if right_is_fist:
                        return 'right'
                else:
                    # No fist required (e.g., for powerups)
                    return 'right'

        return ''

    def check_body_collision(
        self,
        body_points: list,
        object_pos: Tuple[int, int],
        object_radius: int
    ) -> bool:
        """
        Check if any body part collides with an object.

        Args:
            body_points: List of (x, y) body landmark positions
            object_pos: Object center position
            object_radius: Object radius

        Returns:
            bool: True if any body part collides
        """
        for point in body_points:
            if point is not None and self.check_collision(point, object_pos, object_radius):
                return True
        return False

    def check_arm_collision(
        self,
        wrist_pos: Optional[Tuple[int, int]],
        elbow_pos: Optional[Tuple[int, int]],
        object_pos: Tuple[int, int],
        object_radius: int
    ) -> bool:
        """
        Check if arm segment (wrist to elbow) collides with object.

        Args:
            wrist_pos: Wrist position
            elbow_pos: Elbow position
            object_pos: Object center position
            object_radius: Object radius

        Returns:
            bool: True if arm segment intersects with object
        """
        if wrist_pos is None or elbow_pos is None:
            return False

        # Check if object is close to wrist or elbow
        if (self.check_collision(wrist_pos, object_pos, object_radius) or
                self.check_collision(elbow_pos, object_pos, object_radius)):
            return True

        # Check distance from object center to line segment (wrist-elbow)
        # Using point-to-line distance formula
        x0, y0 = object_pos
        x1, y1 = wrist_pos
        x2, y2 = elbow_pos

        # Calculate line segment length
        line_length_sq = (x2 - x1)**2 + (y2 - y1)**2

        if line_length_sq == 0:
            # Wrist and elbow are at same position
            return self.check_collision(wrist_pos, object_pos, object_radius)

        # Calculate projection parameter t
        t = max(0, min(1, ((x0 - x1) * (x2 - x1) +
                (y0 - y1) * (y2 - y1)) / line_length_sq))

        # Find closest point on line segment
        closest_x = x1 + t * (x2 - x1)
        closest_y = y1 + t * (y2 - y1)

        # Calculate distance from object to closest point
        distance = self.point_distance(
            object_pos, (int(closest_x), int(closest_y)))

        return distance < (self.collision_radius + object_radius)
