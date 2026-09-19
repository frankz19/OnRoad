
import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.utilities.highscores import read_highscores


class HighScoreState(BaseState):
    def enter(self) -> None:
        self.hs = read_highscores()
        if "high_score" in settings.SOUNDS:
            settings.SOUNDS["high_score"].play()

    def on_input(self, input_id: str, input_data: InputData):
        if input_id == "confirm" and input_data.pressed:
            self.state_machine.change("title")

    def render(self, surface: pygame.Surface) -> None:

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
            "Mejores Puntajes",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            20,
            (255, 255, 255),
            center=True,
        )

        for i in range(settings.NUM_HIGHSCORES):
            name = "---"
            score = "---"

            if i < len(self.hs):
                item = self.hs[i]
                name = item[0]
                score = str(item[1])

            render_text(
                surface,
                f"{i + 1}.",
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2 - 60,
                50 + i * 17,
                (255, 255, 255),
                center=True,
            )
            render_text(
                surface,
                name,
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2,
                50 + i * 17,
                (255, 255, 255),
                center=True,
            )
            render_text(
                surface,
                score,
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2 + 60,
                50 + i * 17,
                (255, 255, 255),
                center=True,
            )


        render_text(
            surface, "Presiona Enter para continuar!", settings.FONTS["medium"], 
            settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT - 50, 
            (255, 255, 0), center=True
        )