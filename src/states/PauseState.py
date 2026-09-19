# import pygame

# from gale.input_handler import InputData
# from gale.state import BaseState
# from gale.text import render_text

# import settings


# class PauseState(BaseState):
#     def enter(self, **params: dict) -> None:
#         # Recibimos todos los parámetros del juego en curso para poder retomarlos si se reanuda
#         self.play_state_params = params
        
#         # Opcional: pausar la música del juego si lo deseas
#         pygame.mixer.music.pause()

#     def exit(self) -> None:
#         pygame.mixer.music.unpause()

#     def on_input(self, input_id: str, input_data: InputData) -> None:

#         if input_id == "pause" and input_data.pressed:
#             self.state_machine.change("play_onroad", **self.play_state_params)            
#         elif input_id == "confirm" and input_data.pressed:
#             self.state_machine.change("title")

#     def render(self, surface: pygame.Surface) -> None:
#         overlay = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), pygame.SRCALPHA)
#         overlay.fill((0, 0, 0, 160)) # Negro con opacidad
#         surface.blit(overlay, (0, 0))

#         render_text(
#             surface,
#             "JUEGO PAUSADO",
#             settings.FONTS["huge"] if "huge" in settings.FONTS else settings.FONTS["medium"],
#             settings.VIRTUAL_WIDTH // 2,
#             settings.VIRTUAL_HEIGHT // 2 - 40,
#             settings.COLOR_WHITE,
#             center=True,
#         )

#         render_text(
#             surface,
#             "Presiona 'P' para Continuar",
#             settings.FONTS["medium"],
#             settings.VIRTUAL_WIDTH // 2,
#             settings.VIRTUAL_HEIGHT // 2 + 10,
#             (255, 255, 0), # Amarillo brillante
#             center=True,
#         )

#         render_text(
#             surface,
#             "Presiona ENTER para ir al Menu Principal",
#             settings.FONTS["medium"],
#             settings.VIRTUAL_WIDTH // 2,
#             settings.VIRTUAL_HEIGHT // 2 + 40,
#             (200, 200, 200),
#             center=True,
#         )