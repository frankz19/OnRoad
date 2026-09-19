import pygame
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
import settings

class StatsState(BaseState):
    def enter(self, winner: str, reason: str, p1_score: int, p2_score: int) -> None:
        self.winner = winner
        self.reason = reason
        self.p1_score = p1_score
        self.p2_score = p2_score

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(settings.COLOR_BACKGROUND)
        background = settings.TEXTURES["podio12"]
        background_rect = background.get_rect(
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
        render_text(surface, f"{self.winner} Wins!", settings.FONTS["large"], settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 - 60, settings.COLOR_TEXT, center=True)
        render_text(surface, self.reason, settings.FONTS["medium"], settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 - 20, settings.COLOR_TEXT, center=True)
        render_text(surface, f"P1 Score: {self.p1_score} | P2 Score: {self.p2_score}", settings.FONTS["medium"], settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 + 20, settings.COLOR_TEXT, center=True)
        render_text(surface, "Press Enter to return", settings.FONTS["small"], settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 + 60, settings.COLOR_TEXT, center=True)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "confirm" and input_data.pressed:
            self.state_machine.change("title")