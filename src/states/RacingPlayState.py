import pygame
from gale.input_handler import InputData
from gale.physics.world import World
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Bike import Bike
from src.Terrain import Terrain

class FlipPopup:
    def __init__(self, text: str, bike: Bike, color) -> None:
        self.text = text
        self.bike = bike
        self.color = color
        self.scale = 0.3
        self.alpha = 255.0
        self.rise = 0.0
        self.alive = True

class EngineSound:
    def __init__(self, sound: pygame.mixer.Sound, base_volume: float, release_fade: float = 1.0) -> None:
        self.sound = sound
        self.base_volume = base_volume
        self.release_fade = release_fade
        self.channel = None
        self.active = False
        self.fading = False
        self.fade_timer = 0.0
        self.killed = False

    def update(self, wants_sound: bool, dt: float) -> None:
        if self.killed: return
        if wants_sound:
            needs_restart = (not self.active or self.channel is None or not self.channel.get_busy())
            if needs_restart:
                self.sound.stop()
                self.channel = self.sound.play(loops=-1)
                self.active = True
            if self.channel is not None:
                self.channel.set_volume(self.base_volume)
            self.fading = False
            self.fade_timer = 0.0
            return

        if self.active and not self.fading:
            self.fading = True
            self.fade_timer = self.release_fade

        if self.fading:
            self.fade_timer -= dt
            if self.fade_timer <= 0.0:
                if self.channel is not None:
                    self.channel.set_volume(0.0)
                    self.channel.stop()
                self.sound.stop()
                self.channel = None
                self.active = False
                self.fading = False
                self.fade_timer = 0.0
            else:
                if self.channel is not None:
                    vol = self.base_volume * (self.fade_timer / self.release_fade)
                    self.channel.set_volume(vol)

    def stop(self) -> None:
        if self.channel is not None:
            self.channel.set_volume(0.0)
            self.channel.stop()
        self.sound.stop()
        self.channel = None
        self.active = False
        self.fading = False
        self.fade_timer = 0.0
        self.killed = True

    def revive(self) -> None:
        self.killed = False


class RacingPlayState(BaseState):
    def enter(self) -> None:
        settings.randomize_terrain()
        settings.stop_all_audio()

        self.world_p1 = World(gravity=settings.GRAVITY)
        self.world_p2 = World(gravity=settings.GRAVITY)

        self.terrain_p1 = Terrain(self.world_p1)
        self.terrain_p2 = Terrain(self.world_p2)

        self.surf_w = settings.VIRTUAL_WIDTH
        self.surf_h = settings.VIRTUAL_HEIGHT // 2

        # Incrementamos el área renderizada para alejar la cámara (factor de zoom 2.2)
        self.zoom = 3
        self.cam_w = int(self.surf_w * self.zoom)
        self.cam_h = int(self.surf_h * self.zoom)

        raw_background = settings.TEXTURES["racing_background"] 
        aspect_ratio = self.cam_h / raw_background.get_height()
        new_width = int(raw_background.get_width() * aspect_ratio)
        self.scaled_background = pygame.transform.scale(
            raw_background, (new_width, self.cam_h)
        )

        start_x = 100
        start_y = settings.terrain_height(start_x) - 100

        self.p1_bike = Bike(self.world_p1, start_x, start_y, "TextureR1", "p1")
        self.p2_bike = Bike(self.world_p2, start_x, start_y, "TextureSDT", "p2")

        self.inputs = {
            "p1_accel": False, "p1_brake": False,
            "p1_tilt_fwd": False, "p1_tilt_back": False,
            "p2_accel": False, "p2_brake": False,
            "p2_tilt_fwd": False, "p2_tilt_back": False,
        }
        self.ended = False
        self.paused = False
        self.first_finisher = None
        self.timeout_timer = 10.0

        # Superficies de mayor resolución para dibujar antes de escalar
        self.surf_p1 = pygame.Surface((self.cam_w, self.cam_h))
        self.surf_p2 = pygame.Surface((self.cam_w, self.cam_h))

        pygame.mixer.music.load(settings.MUSIC_PATH)
        pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
        pygame.mixer.music.play(loops=-1)

        settings.SOUNDS["bonus"].set_volume(settings.BONUS_VOLUME)
        self.p1_engine = EngineSound(settings.SOUNDS["r1_engine"], settings.ENGINE_VOLUME)
        self.p2_engine = EngineSound(settings.SOUNDS["sdt_engine"], settings.ENGINE_VOLUME)
        self.p1_engine.revive()
        self.p2_engine.revive()

        self.p1_popups = []
        self.p2_popups = []

        self.countdown_active = True
        self.countdown_time = 3.0
        self.countdown_text = "3"
        self.countdown_scale = 0.3
        self.countdown_alpha = 255.0
        self._countdown_pop()

        self.world_p1.on_collision_begin(self._on_collision_begin)
        self.world_p2.on_collision_begin(self._on_collision_begin)

    def exit(self) -> None:
        self.p1_engine.stop()
        self.p2_engine.stop()
        settings.stop_all_audio()
        Timer.clear()

    def _countdown_pop(self) -> None:
        self.countdown_scale = 0.3
        self.countdown_alpha = 255.0
        Timer.tween(0.3, [(self, {"countdown_scale": 1.0})], ease_function_name="out_back")

    def _update_countdown(self, dt: float) -> None:
        self.countdown_time -= dt
        if self.countdown_time > 2.0:
            new_text, segment_left = "3", self.countdown_time - 2.0
        elif self.countdown_time > 1.0:
            new_text, segment_left = "2", self.countdown_time - 1.0
        elif self.countdown_time > 0.0:
            new_text, segment_left = "1", self.countdown_time
        else:
            new_text, segment_left = "GO!", 0.7 + self.countdown_time
            if self.countdown_time < -0.7:
                self.countdown_active = False
                return

        if new_text != self.countdown_text:
            self.countdown_text = new_text
            self._countdown_pop()
        else:
            if new_text == "GO!":
                self.countdown_alpha = 255 * max(0.0, min(1.0, segment_left / 0.7))
            elif segment_left < 0.2:
                self.countdown_alpha = 255 * (segment_left / 0.2)
            else:
                self.countdown_alpha = 255.0

    def _render_countdown(self, surface: pygame.Surface) -> None:
        text_surf = settings.FONTS["large"].render(self.countdown_text, True, (255, 255, 255))
        scaled = pygame.transform.rotozoom(text_surf, 0, self.countdown_scale * 3.0)
        alpha = max(0, min(255, int(self.countdown_alpha)))
        if alpha < 255:
            scaled.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        rect = scaled.get_rect(center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2))
        surface.blit(scaled, rect.topleft)

    def _spawn_flip_popup(self, flips: int, bike: Bike, popups: list) -> None:
        degrees = flips * 360
        if degrees >= 1440: color = settings.COLOR_FLIP_MAX
        elif degrees >= 1080: color = settings.COLOR_FLIP_1080
        elif degrees >= 720: color = settings.COLOR_FLIP_720
        else: color = settings.COLOR_FLIP_360

        popup = FlipPopup(f"{degrees} o", bike, color)
        popups.append(popup)
        settings.SOUNDS["bonus"].play()

        Timer.tween(
            0.25, [(popup, {"scale": 1.4})], ease_function_name="out_back",
            on_finish=lambda p=popup: Timer.tween(
                1.0, [(p, {"scale": 1.1, "rise": -80.0, "alpha": 0.0})],
                ease_function_name="out_quad", on_finish=lambda p=p: setattr(p, "alive", False)
            )
        )

    def _on_collision_begin(self, body_a, body_b):
        if self.ended: return
        tags = {body_a.user_data, body_b.user_data}
        if "terrain" in tags:
            if "rider_p1" in tags: self._end_game("Player 2", "Player 1 crashed!")
            elif "rider_p2" in tags: self._end_game("Player 1", "Player 2 crashed!")

    def _end_game(self, winner: str, reason: str):
        if self.ended: return
        self.ended = True
        self.p1_engine.stop()
        self.p2_engine.stop()
        settings.stop_all_audio()
        self.state_machine.change(
            "stats_racing", winner=winner, reason=reason,
            p1_score=self.p1_bike.score, p2_score=self.p2_bike.score
        )

    def update(self, dt: float) -> None:
        if self.ended: return
        self.p1_popups = [p for p in self.p1_popups if p.alive]
        self.p2_popups = [p for p in self.p2_popups if p.alive]

        if self.paused:
            self.p1_engine.stop()
            self.p2_engine.stop()
            return

        if self.countdown_active:
            self._update_countdown(dt)
            self.p1_bike.drive(0)
            self.p2_bike.drive(0)
            self.p1_bike.tilt(0)
            self.p2_bike.tilt(0)
            self.p1_bike.update(dt)
            self.p2_bike.update(dt)
            self.world_p1.update(dt)
            self.world_p2.update(dt)
            self.p1_engine.update(False, dt)
            self.p2_engine.update(False, dt)
            return

        p1_drive = int(self.inputs["p1_accel"]) - int(self.inputs["p1_brake"])
        p1_tilt = int(self.inputs["p1_tilt_fwd"]) - int(self.inputs["p1_tilt_back"])
        self.p1_bike.drive(p1_drive)
        self.p1_bike.tilt(p1_tilt)
        self.p1_bike.update(dt)

        p2_drive = int(self.inputs["p2_accel"]) - int(self.inputs["p2_brake"])
        p2_tilt = int(self.inputs["p2_tilt_fwd"]) - int(self.inputs["p2_tilt_back"])
        self.p2_bike.drive(p2_drive)
        self.p2_bike.tilt(p2_tilt)
        self.p2_bike.update(dt)

        self.world_p1.update(dt)
        self.world_p2.update(dt)

        if self.ended: return

        self.p1_engine.update(self.inputs["p1_accel"], dt)
        self.p2_engine.update(self.inputs["p2_accel"], dt)

        if self.p1_bike.pending_flip > 0:
            self._spawn_flip_popup(self.p1_bike.pending_flip, self.p1_bike, self.p1_popups)
            self.p1_bike.pending_flip = 0

        if self.p2_bike.pending_flip > 0:
            self._spawn_flip_popup(self.p2_bike.pending_flip, self.p2_bike, self.p2_popups)
            self.p2_bike.pending_flip = 0

        if self.p1_bike.chassis.position.x < -50:
            self._end_game("Player 2", "Player 1 fell at the start!")
            return
        if self.p2_bike.chassis.position.x < -50:
            self._end_game("Player 1", "Player 2 fell at the start!")
            return

        p1_reached = self.p1_bike.chassis.position.x >= settings.GOAL_X
        p2_reached = self.p2_bike.chassis.position.x >= settings.GOAL_X
        fall_limit = settings.VIRTUAL_HEIGHT + 200

        if self.p1_bike.chassis.position.y > fall_limit and not p1_reached:
            self._end_game("Player 2", "Player 1 fell into the void!")
            return
        if self.p2_bike.chassis.position.y > fall_limit and not p2_reached:
            self._end_game("Player 1", "Player 2 fell into the void!")
            return

        if not self.first_finisher:
            if p1_reached and p2_reached:
                self.first_finisher = "Player 1"
                self.p1_bike.score += 720
            elif p1_reached:
                self.first_finisher = "Player 1"
                self.p1_bike.score += 720
            elif p2_reached:
                self.first_finisher = "Player 2"
                self.p2_bike.score += 720

        if self.first_finisher:
            if (self.first_finisher == "Player 1" and p2_reached) or (self.first_finisher == "Player 2" and p1_reached):
                winner = "Player 1" if self.p1_bike.score >= self.p2_bike.score else "Player 2"
                self._end_game(winner, "Both Finished! (Score decides)")
            else:
                self.timeout_timer -= dt
                if self.timeout_timer <= 0:
                    loser = "Player 2" if self.first_finisher == "Player 1" else "Player 1"
                    self._end_game(self.first_finisher, f"Time out for {loser}!")

    def render(self, surface: pygame.Surface) -> None:
        self.surf_p1.fill(settings.COLOR_BACKGROUND)
        self.surf_p2.fill(settings.COLOR_BACKGROUND)

        bg_p1_x = -(self.p1_bike.chassis.position.x / 2.5) % self.scaled_background.get_width()
        bg_p2_x = -(self.p2_bike.chassis.position.x / 2.5) % self.scaled_background.get_width()

        self.surf_p1.blit(self.scaled_background, (bg_p1_x, 0))
        self.surf_p1.blit(self.scaled_background, (bg_p1_x - self.scaled_background.get_width(), 0))
        self.surf_p2.blit(self.scaled_background, (bg_p2_x, 0))
        self.surf_p2.blit(self.scaled_background, (bg_p2_x - self.scaled_background.get_width(), 0))

        cam_p1_x, cam_p1_y = self.p1_bike.chassis.position.x, self.p1_bike.chassis.position.y
        if cam_p1_x > settings.GOAL_X + 150:
            cam_p1_x = settings.GOAL_X + 150
            cam_p1_y = min(cam_p1_y, settings.terrain_height(settings.GOAL_X))

        cam_p2_x, cam_p2_y = self.p2_bike.chassis.position.x, self.p2_bike.chassis.position.y
        if cam_p2_x > settings.GOAL_X + 150:
            cam_p2_x = settings.GOAL_X + 150
            cam_p2_y = min(cam_p2_y, settings.terrain_height(settings.GOAL_X))

        offset_p1_x, offset_p1_y = cam_p1_x - (self.cam_w / 2), cam_p1_y - (self.cam_h / 2)
        offset_p2_x, offset_p2_y = cam_p2_x - (self.cam_w / 2), cam_p2_y - (self.cam_h / 2)

        self.terrain_p1.render(self.surf_p1, offset_p1_x, offset_p1_y)
        self.p2_bike.render(self.surf_p1, offset_p1_x, offset_p1_y)
        self.p1_bike.render(self.surf_p1, offset_p1_x, offset_p1_y)

        self.terrain_p2.render(self.surf_p2, offset_p2_x, offset_p2_y)
        self.p1_bike.render(self.surf_p2, offset_p2_x, offset_p2_y)
        self.p2_bike.render(self.surf_p2, offset_p2_x, offset_p2_y)

        self._render_popups(self.surf_p1, self.p1_popups, offset_p1_x, offset_p1_y)
        self._render_popups(self.surf_p2, self.p2_popups, offset_p2_x, offset_p2_y)

        # Escalar las vistas virtuales grandes de nuevo a la resolución final para un efecto de zoom out
        scaled_p1 = pygame.transform.smoothscale(self.surf_p1, (self.surf_w, self.surf_h))
        scaled_p2 = pygame.transform.smoothscale(self.surf_p2, (self.surf_w, self.surf_h))

        surface.blit(scaled_p1, (0, 0))
        surface.blit(scaled_p2, (0, self.surf_h))

        pygame.draw.line(surface, settings.COLOR_TEXT, (0, self.surf_h), (self.surf_w, self.surf_h), 4)

        render_text(surface, f"P1 Score: {self.p1_bike.score}", settings.FONTS["medium"], 20, 20, settings.COLOR_P1)
        render_text(surface, f"P2 Score: {self.p2_bike.score}", settings.FONTS["medium"], 20, self.surf_h + 20, settings.COLOR_P2)

        if self.first_finisher and not self.ended:
            render_text(surface, f"TIME LIMIT: {max(0, self.timeout_timer):.1f}s!", settings.FONTS["large"], self.surf_w / 2, self.surf_h, settings.COLOR_ALERT, center=True)

        if self.countdown_active:
            self._render_countdown(surface)

        if self.paused:
            overlay = pygame.Surface((self.surf_w, settings.VIRTUAL_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))
            render_text(surface, "PAUSED", settings.FONTS["large"], self.surf_w / 2, settings.VIRTUAL_HEIGHT / 2, settings.COLOR_ALERT, center=True)

    def _render_popups(self, surface: pygame.Surface, popups: list, offset_x: float, offset_y: float) -> None:
        for popup in popups:
            if not popup.alive: continue
            screen_x = popup.bike.chassis.position.x - offset_x
            screen_y = popup.bike.chassis.position.y - 70 + popup.rise - offset_y

            # Limitamos la renderización usando cam_w y cam_h para que cubra la superficie ampliada
            if not (-250 < screen_x < self.cam_w + 250 and -250 < screen_y < self.cam_h + 250):
                continue

            text_surf = settings.FONTS["large"].render(popup.text, True, popup.color)
            scaled = pygame.transform.rotozoom(text_surf, 0, popup.scale)
            alpha = max(0, min(255, int(popup.alpha)))
            if alpha < 255: scaled.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
            rect = scaled.get_rect(center=(int(screen_x), int(screen_y)))
            surface.blit(scaled, rect.topleft)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if self.ended: return
        if input_id == "pause" and input_data.pressed:
            self.paused = not self.paused
            pygame.mixer.music.set_volume(settings.MUSIC_VOLUME * (0.3 if self.paused else 1.0))
            return

        if self.paused: return
        val = 1 if input_data.pressed else 0

        if input_id == "p1_accel": self.inputs["p1_accel"] = val
        elif input_id == "p1_brake": self.inputs["p1_brake"] = val
        elif input_id == "p1_tilt_fwd": self.inputs["p1_tilt_fwd"] = val
        elif input_id == "p1_tilt_back": self.inputs["p1_tilt_back"] = val
        elif input_id == "p2_accel": self.inputs["p2_accel"] = val
        elif input_id == "p2_brake": self.inputs["p2_brake"] = val
        elif input_id == "p2_tilt_fwd": self.inputs["p2_tilt_fwd"] = val
        elif input_id == "p2_tilt_back": self.inputs["p2_tilt_back"] = val