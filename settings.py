import os
import math
import random
from pathlib import Path
import pygame
from gale import input_handler

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "confirm")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_p, "pause")

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_1, "mode_1")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_2, "mode_2")

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SPACE, "willy")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_UP, "up")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_DOWN, "down")

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_w, "p1_accel")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_s, "p1_brake")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_a, "p1_tilt_back")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_d, "p1_tilt_fwd")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_UP, "p2_accel")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_DOWN, "p2_brake")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "p2_tilt_back")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "p2_tilt_fwd")

TITLE = "OnRoad & Freestyle Racing"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
VIRTUAL_WIDTH = 512
VIRTUAL_HEIGHT = 288


MAIN_SCROLL_SPEED = 100
BACK_SCROLL_SPEED = 50
BIKE_WIDTH = 62
BIKE_HEIGHT = 34
HORIZONTAL_SPEED = 120
BIKE_SPEED_BASE = 150
FUEL_MAX = 100
FUEL_CONSUMPTION_RATE = 5
TIRE_WEAR_RATE = 2
BACKGROUND_LOOPING_POINT = 528
TRACK_TOP = 160
TRACK_BOTTOM = VIRTUAL_HEIGHT - BIKE_HEIGHT
TRACK_HEIGHT = VIRTUAL_HEIGHT - TRACK_TOP
OBSTACLE_WIDTH = 47
OBSTACLE_HEIGHT = 32
NUM_HIGHSCORES = 10


GRAVITY = (0, 900)
MAP_LENGTH = VIRTUAL_WIDTH * 20
GOAL_X = MAP_LENGTH - 200
FLAT_START = 600
FLAT_TRANSITION = 250
TERRAIN_BASE_Y = 300
TERRAIN_STEP = 20
TERRAIN_FRICTION = 1.5


CHASSIS_WIDTH, CHASSIS_HEIGHT = 80, 18
CHASSIS_DENSITY = 1.3

RIDER_HEIGHT = 14
RIDER_DENSITY = 0.5
WHEEL_RADIUS = 16

WHEEL_OFFSET_X, WHEEL_OFFSET_Y = 28, 24

WHEEL_FRICTION = 2.5
WHEEL_DENSITY = 0.8

SUSPENSION_FREQUENCY = 4.5
SUSPENSION_DAMPING = 0.75


BALLAST_WIDTH = 20
BALLAST_HEIGHT = 14
BALLAST_DENSITY = 3.0
BALLAST_OFFSET_X = 25


MOTOR_SPEED = 50.0
MOTOR_TORQUE = 70


TILT_TORQUE = 60


GROUND_STABILITY = 550
GROUND_ANGULAR_DAMPING = 30
GROUND_GRACE_TIME = 0.05


WHEELIE_COUNTER_RATIO = 1.5

AIR_ANGULAR_DAMPING = 0.1
AIR_MAX_ROTATION = 15.0
AIR_ROTATION_GAIN = 100
AIR_TILT_TORQUE = 800
FLIP_TOLERANCE = 0.25
FLIP_SCORE = 250

COLOR_BACKGROUND = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_TERRAIN = (100, 110, 120)
COLOR_P1 = (90, 200, 255)
COLOR_P2 = (255, 90, 120)
COLOR_TEXT = (255, 255, 255)
COLOR_ALERT = (255, 80, 80)
COLOR_FLIP_360 = (255, 255, 255)
COLOR_FLIP_720 = (255, 220, 80)
COLOR_FLIP_1080 = (255, 120, 60)
COLOR_FLIP_MAX = (255, 60, 220)


BASE_DIR = Path(__file__).parent

MEDIUM_TEXT_SIZE = 18
HUGE_TEXT_SIZE = 56
ONROAD_TEXT_SIZE = 28

obstacles_sheet = pygame.image.load(BASE_DIR / "assets" / "graphics" / "obstacles.png")

FRAMES = {
    "obstacles": [
        obstacles_sheet.subsurface(pygame.Rect(0, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
        obstacles_sheet.subsurface(pygame.Rect(47, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
        obstacles_sheet.subsurface(pygame.Rect(94, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
        obstacles_sheet.subsurface(pygame.Rect(141, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
    ],
}

raw_r1 = pygame.image.load(BASE_DIR / "assets" / "graphics" / "TextureR1.png")
raw_sdt = pygame.image.load(BASE_DIR / "assets" / "graphics" / "TextureSuperDT.png")
scaled_r1 = pygame.transform.scale(raw_r1, (110, 60))
scaled_sdt = pygame.transform.scale(raw_sdt, (110, 60))

TEXTURES = {
    "fuel": pygame.image.load(BASE_DIR / "assets" / "graphics" / "fuel.png"),
    "bike": pygame.image.load(BASE_DIR / "assets" / "graphics" / "bike.png"),
    "bike_1": pygame.image.load(BASE_DIR / "assets" / "graphics" / "bike 2.png"),
    "bike_2": pygame.image.load(BASE_DIR / "assets" / "graphics" / "bike 3.png"),
    "bike_3": pygame.image.load(BASE_DIR / "assets" / "graphics" / "bike 4.png"),
    "background": pygame.transform.scale(
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "background.jpg"),
        (BACKGROUND_LOOPING_POINT, VIRTUAL_HEIGHT)
    ),
    "ground": pygame.transform.scale(
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "Carretera.png"),
        (1024, TRACK_HEIGHT)
    ),
    "title_image": pygame.transform.scale(
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "ONROAD.png"),
        (BACKGROUND_LOOPING_POINT, VIRTUAL_HEIGHT)
    ),
    "game_over": pygame.transform.scale(
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "game_over.jpg"),
        (BACKGROUND_LOOPING_POINT, VIRTUAL_HEIGHT)
    ),
    "garage": pygame.transform.scale(
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "garage.jpg"),
        (BACKGROUND_LOOPING_POINT, VIRTUAL_HEIGHT)
    ),
    "podio": pygame.transform.scale(
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "podio.jpg"),
        (BACKGROUND_LOOPING_POINT, VIRTUAL_HEIGHT)
    ),
    "podio12": pygame.transform.scale(
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "podio12.jpg"),
        (BACKGROUND_LOOPING_POINT, VIRTUAL_HEIGHT)
    ),
    "racing_background": pygame.image.load(BASE_DIR / "assets" / "graphics" / "racing_background.png"),
    "TextureR1": scaled_r1,
    "TextureSDT": scaled_sdt,
}

pygame.mixer.set_num_channels(16)

SOUNDS = {
    "explosion": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "explosion.wav"),
    "boost": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "boost.mp3"),
    "high_score": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "highscore.mp3"),
    "score": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "score.wav"),
    "hurt": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "hurt.wav"),
    "game_over": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "game_over.mp3"),
    "bonus": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "bonus.wav"),
    "r1_engine": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "R1accelerating.wav"),
    "sdt_engine": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "SDTaccelerating.wav"),
}

MUSIC_PATH = BASE_DIR / "assets" / "sounds" / "RaceSoundTrack.mp3"
MUSIC_VOLUME = 0.4
ENGINE_VOLUME = 0.5
BONUS_VOLUME = 0.8

ONROAD_MUSIC_PATH = BASE_DIR / "assets" / "sounds" / "TitleMusic.mp3"
ONROAD_MUSIC_VOLUME = 0.4

FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 12),
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", MEDIUM_TEXT_SIZE),
    "huge": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", HUGE_TEXT_SIZE),
    "large": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", 24),
    "onroad": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "flappy.ttf", ONROAD_TEXT_SIZE),
}

MAP_OFFSET = 0.0


def randomize_terrain():
    global MAP_OFFSET
    MAP_OFFSET = random.uniform(0, 10000.0)


def stop_all_audio():
    pygame.mixer.music.stop()
    for i in range(pygame.mixer.get_num_channels()):
        channel = pygame.mixer.Channel(i)
        channel.set_volume(0.0)
        channel.stop()
    for sound in SOUNDS.values():
        sound.stop()
    pygame.mixer.stop()


def terrain_height(x: float) -> float:
    shifted_x = x + MAP_OFFSET
    smooth_hill = 40 * math.sin(shifted_x * 0.0015)
    extreme_peak = 250 * math.pow(math.sin(shifted_x * 0.0022), 8)
    natural_height = TERRAIN_BASE_Y - smooth_hill - extreme_peak

    if x < FLAT_START:
        return TERRAIN_BASE_Y

    if x < FLAT_START + FLAT_TRANSITION:
        t = (x - FLAT_START) / FLAT_TRANSITION
        t = t * t * (3 - 2 * t)
        return TERRAIN_BASE_Y * (1 - t) + natural_height * t

    return natural_height