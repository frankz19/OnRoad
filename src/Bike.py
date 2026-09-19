import math
import pygame
from gale.physics.shapes import BoxShape, CircleShape, PolygonShape
from gale.physics.world import World
import settings


class Bike:
    def __init__(self, world: World, x: float, y: float,
                 texture_key: str, player_id: str) -> None:
        self.texture_key = texture_key
        self.score = 0
        self.player_id = player_id
        self.current_drive = 0

        self.pending_flip = 0


        self.chassis = world.create_dynamic_body(
            x, y,
            BoxShape(settings.CHASSIS_WIDTH, settings.CHASSIS_HEIGHT,
                     density=settings.CHASSIS_DENSITY),
        )
        self.chassis.user_data = f"chassis_{player_id}"


        self.chassis.add_box(BoxShape(
            settings.BALLAST_WIDTH,
            settings.BALLAST_HEIGHT,
            density=settings.BALLAST_DENSITY,
            offset=(settings.BALLAST_OFFSET_X, 0),
        ))


        rider_w = settings.CHASSIS_WIDTH * 0.5
        rider_h = settings.RIDER_HEIGHT
        ry = -settings.CHASSIS_HEIGHT / 2 - rider_h / 2 - 1
        self.rider_points = [
            (-rider_w / 2, ry - rider_h / 2),
            (rider_w / 2, ry - rider_h / 2),
            (rider_w / 2, ry + rider_h / 2),
            (-rider_w / 2, ry + rider_h / 2),
        ]
        self.rider = world.create_dynamic_body(
            x, y,
            PolygonShape(self.rider_points,
                         density=settings.RIDER_DENSITY,
                         is_sensor=True),
        )
        self.rider.user_data = f"rider_{player_id}"

        self.rider_joint = world.create_revolute_joint(
            self.chassis, self.rider, self.chassis.position,
            enable_limit=True, lower_angle=0.0, upper_angle=0.0,
        )

        wheel_y = y + settings.WHEEL_OFFSET_Y
        self.rear_wheel = world.create_dynamic_body(
            x - settings.WHEEL_OFFSET_X, wheel_y,
            CircleShape(radius=settings.WHEEL_RADIUS,
                        friction=settings.WHEEL_FRICTION,
                        density=settings.WHEEL_DENSITY),
        )
        self.rear_wheel.user_data = "wheel"

        self.front_wheel = world.create_dynamic_body(
            x + settings.WHEEL_OFFSET_X, wheel_y,
            CircleShape(radius=settings.WHEEL_RADIUS,
                        friction=settings.WHEEL_FRICTION,
                        density=settings.WHEEL_DENSITY),
        )
        self.front_wheel.user_data = "wheel"


        self.rear_joint = world.create_wheel_joint(
            self.chassis, self.rear_wheel, self.rear_wheel.position,
            axis=(0, 1),
            frequencyHz=settings.SUSPENSION_FREQUENCY,
            dampingRatio=settings.SUSPENSION_DAMPING,
        )
        self.front_joint = world.create_wheel_joint(
            self.chassis, self.front_wheel, self.front_wheel.position,
            axis=(0, 1),
            frequencyHz=settings.SUSPENSION_FREQUENCY,
            dampingRatio=settings.SUSPENSION_DAMPING,
        )

        self.rear_joint.enable_motor = True
        self.rear_joint.max_motor_torque = settings.MOTOR_TORQUE
        self.rear_joint.motor_speed = 0
        self.front_joint.enable_motor = False


        self._counter_torque = (
            settings.MOTOR_TORQUE * settings.WHEELIE_COUNTER_RATIO
        )


        self.last_angle = self.chassis.angle
        self.accumulated_rotation = 0.0
        self.was_airborne = False
        self._airborne_time = 0.0

        self._max_flips_in_flight = 0


    def _has_wheel_contact(self) -> bool:
        for wheel in (self.rear_wheel, self.front_wheel):
            for body in wheel.touching_bodies:
                if body.user_data == "terrain":
                    return True
        return False

    def is_grounded(self) -> bool:
        return (self._has_wheel_contact()
                or self._airborne_time < settings.GROUND_GRACE_TIME)


    def _terrain_slope_angle(self) -> float:
        rear_x = self.rear_wheel.position.x
        front_x = self.front_wheel.position.x
        rear_y = settings.terrain_height(rear_x)
        front_y = settings.terrain_height(front_x)
        dx = front_x - rear_x
        if abs(dx) < 1e-6:
            return 0.0
        return math.atan2(front_y - rear_y, dx)

    def _apply_ground_stability(self) -> None:
        target = self._terrain_slope_angle()
        error = target - self.chassis.angle

        while error > math.pi:
            error -= 2 * math.pi
        while error < -math.pi:
            error += 2 * math.pi

        torque = (
            error * settings.GROUND_STABILITY
            - self.chassis.angular_velocity * settings.GROUND_ANGULAR_DAMPING
        )
        self.chassis.apply_torque(torque)


    def _apply_air_control(self) -> None:
        self.chassis.apply_torque(
            -self.chassis.angular_velocity * settings.AIR_ANGULAR_DAMPING
        )


    def update(self, dt: float) -> None:

        delta = self.chassis.angle - self.last_angle
        while delta > math.pi:
            delta -= 2 * math.pi
        while delta < -math.pi:
            delta += 2 * math.pi
        self.accumulated_rotation += delta
        self.last_angle = self.chassis.angle


        if self._has_wheel_contact():
            self._airborne_time = 0.0
        else:
            self._airborne_time += dt

        grounded = self.is_grounded()

        if grounded:

            if self.was_airborne:
                flips = self._max_flips_in_flight
                if flips > 0 and self.chassis.position.x < settings.GOAL_X:
                    self.score += flips * settings.FLIP_SCORE
                    self.pending_flip = flips
                self.accumulated_rotation = 0.0
                self._max_flips_in_flight = 0
            self.was_airborne = False
            self._apply_ground_stability()
        else:

            current_flips = int(
                abs(self.accumulated_rotation) / (2 * math.pi)
                + settings.FLIP_TOLERANCE
            )
            if current_flips > self._max_flips_in_flight:
                self._max_flips_in_flight = current_flips

            self.was_airborne = True
            self._apply_air_control()

        # --- ANTI-WHEELIE ---
        if grounded and self.current_drive != 0:
            self.chassis.apply_torque(
                self.current_drive * self._counter_torque
            )


    def drive(self, direction: int) -> None:
        self.current_drive = direction
        self.rear_joint.motor_speed = direction * settings.MOTOR_SPEED

    def tilt(self, direction: int) -> None:
        if self.is_grounded():
            self.chassis.apply_torque(direction * settings.TILT_TORQUE)
            return

        if direction == 0:
            return

        target_rot = direction * settings.AIR_MAX_ROTATION
        error = target_rot - self.chassis.angular_velocity
        torque = error * settings.AIR_ROTATION_GAIN

        if torque > settings.AIR_TILT_TORQUE:
            torque = settings.AIR_TILT_TORQUE
        elif torque < -settings.AIR_TILT_TORQUE:
            torque = -settings.AIR_TILT_TORQUE

        self.chassis.apply_torque(torque)


    def render(self, surface: pygame.Surface, offset_x: float, offset_y: float) -> None:
        image = settings.TEXTURES[self.texture_key]

        angle_degrees = math.degrees(-self.chassis.angle)
        rotated_image = pygame.transform.rotate(image, angle_degrees)

        base_x = self.chassis.position.x - offset_x
        base_y = self.chassis.position.y - offset_y

        y_adjust = 10

        shift_x = math.sin(self.chassis.angle) * y_adjust
        shift_y = math.cos(self.chassis.angle) * y_adjust

        center_x = base_x + shift_x
        center_y = base_y + shift_y

        rect = rotated_image.get_rect(center=(center_x, center_y))
        surface.blit(rotated_image, rect.topleft)

    def _rotate(self, x, y, angle):
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return x * cos_a - y * sin_a, x * sin_a + y * cos_a