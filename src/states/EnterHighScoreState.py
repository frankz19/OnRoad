import string

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
import src.utilities.highscores as HighScore


class EnterHighScoreState(BaseState):
    def enter(self, score: int) -> None:
        self.score = score
        self.hs = HighScore.read_highscores()

        if len(self.hs) < settings.NUM_HIGHSCORES or self.score > self.hs[-1][1]:
            self.chars = [65, 65, 65] # Códigos ASCII para A, A, A
            self.highlighted_char = 0
        else:
            self.state_machine.change("high_score")

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "confirm" and input_data.pressed:
            name = "".join([chr(c) for c in self.chars])
            HighScore.add_high_score(self.hs, name, self.score)
            HighScore.save_high_scores(self.hs)
            self.state_machine.change("high_score")

        elif input_id in ("left", "p1_tilt_back", "p2_tilt_back") and input_data.pressed:
            self.highlighted_char = max(0, self.highlighted_char - 1)
        elif input_id in ("right", "p1_tilt_fwd", "p2_tilt_fwd") and input_data.pressed:
            self.highlighted_char = min(2, self.highlighted_char + 1)
        elif input_id in ("up", "p1_accel", "p2_accel") and input_data.pressed:
            self.chars[self.highlighted_char] = self.chars[self.highlighted_char] + 1
            if self.chars[self.highlighted_char] > 90: # Pasa de la Z a la A
                self.chars[self.highlighted_char] = 65
        elif input_id in ("down", "p1_brake", "p2_brake") and input_data.pressed:
            self.chars[self.highlighted_char] = self.chars[self.highlighted_char] - 1
            if self.chars[self.highlighted_char] < 65: # Pasa de la A a la Z
                self.chars[self.highlighted_char] = 90

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(settings.COLOR_BACKGROUND)

        background = settings.TEXTURES["podio"]
        background_rect = background.get_rect(
            # Mitad exacta de la pantalla en ambos ejes
            center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2) 
        )
        
        surface.blit(background, background_rect)

        overlay_width = 300
        overlay_height = 400
        overlay_surface = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
        # Color negro con opacidad (150 de 255 para que oscurezca pero se siga viendo el fondo)
        overlay_surface.fill((0, 0, 0, 150)) 

        # Posicionarlo centrado en la pantalla
        overlay_rect = overlay_surface.get_rect(center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 - 5))
        surface.blit(overlay_surface, overlay_rect)
        render_text(
            surface,
            f"Puntaje Final: {self.score}",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 - 100,
            (255, 255, 255),
            center=True,
        )
        render_text(
            surface,
            f"Estas entre los mejores {settings.NUM_HIGHSCORES}!",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 - 70,
            (255, 255, 255),
            center=True,
        )
        render_text(
            surface,
            "Ingresa tus iniciales",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 - 20,
            (255, 255, 255),
            center=True,
        )

        x = settings.VIRTUAL_WIDTH // 2 - 20

        for i in range(3):
            color = (52, 235, 216) if self.highlighted_char == i else (255, 255, 255)

            render_text(
                surface,
                chr(self.chars[i]),
                settings.FONTS["medium"],
                x,
                settings.VIRTUAL_HEIGHT // 2,
                color,
                center=True,
            )

            x += 20

        render_text(
            surface,
            "Presiona Enter para finalizar!",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT - 50,
            (255, 255, 255),
            center=True,
        )