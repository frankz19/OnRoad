import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings


class TitleScreenState(BaseState):
    def enter(self) -> None:
        # 1. Matar cualquier audio residual que haya quedado de la
        #    partida anterior (motores, bonus, explosiones, música...).
        settings.stop_all_audio()

        # 2. Arrancar la música del título, siempre que se entra aquí.
        #    Antes vivía en OnRoad.init(), pero eso solo lo ejecutaba
        #    UNA VEZ al arrancar el juego: al morir y volver al título,
        #    nadie la reiniciaba y el menú quedaba en silencio.
        pygame.mixer.music.load(settings.ONROAD_MUSIC_PATH)
        pygame.mixer.music.set_volume(settings.ONROAD_MUSIC_VOLUME)
        pygame.mixer.music.play(loops=-1)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(settings.COLOR_BACKGROUND)

        logo = settings.TEXTURES["title_image"]
        logo_rect = logo.get_rect(
            center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2)
        )
        surface.blit(logo, logo_rect)

        render_text(
            surface,
            "Presiona 1: Modo Esquivar (1 Jugador)",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 1.5 + 50,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            "Presiona 2: Modo Piruetas (2 Jugadores)",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 1.5 + 80,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_data.pressed:
            if input_id == "mode_1":
                self.state_machine.change("bike_select")
            elif input_id == "mode_2":
                self.state_machine.change("play_racing")