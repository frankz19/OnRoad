import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text


import settings
import src.utilities.highscores as HighScore


class GameOverState(BaseState):
    def enter(self, score: int) -> None:
        self.score = score
        self.unlocked_message = None
        if "game_over" in settings.SOUNDS:
            settings.SOUNDS["game_over"].play()

        hs = HighScore.read_highscores()
        
        previous_max_score = hs[0][1] if hs else 0

        bikes_info = {
            1: ("SBR Desbloqueada!", 250),
            2: ("Enduro Desbloqueada!", 500),
            3: ("Hyper Beast Desbloqueada!", 800)
        }

        for bike_id, (msg, threshold) in bikes_info.items():
            if self.score >= threshold and previous_max_score < threshold:
                self.unlocked_message = msg
                break

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "confirm" and input_data.pressed:
            self.state_machine.change("enter_high_score", score=self.score)

    def render(self, surface: pygame.Surface) -> None:


        surface.fill(settings.COLOR_BACKGROUND)
        
        background = settings.TEXTURES["game_over"]
        background_rect = background.get_rect(

            center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2) 
        )
        surface.blit(background, background_rect)

        
        overlay_width = 300
        overlay_height = 120
        overlay_height = 140 if self.unlocked_message else 120
        overlay_surface = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 150)) 


        overlay_rect = overlay_surface.get_rect(center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 - 5))
        surface.blit(overlay_surface, overlay_rect)

      
        render_text(
            surface, "Game Over", settings.FONTS["large"], 
            settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 - 30, 
            (255, 255, 255), center=True
        )
        render_text(
            surface, f"Puntaje Final: {self.score}", settings.FONTS["medium"], 
            settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2, 
            (255, 255, 255), center=True
        )
        


        render_text(
            surface, "Presiona Enter para continuar!", settings.FONTS["medium"], 
            settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 + 20, 
            (255, 255, 0), center=True
        )

        if self.unlocked_message:
            render_text(
                surface, self.unlocked_message, settings.FONTS["medium"], 
                settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 + 50, 
                (255, 215, 0), center=True  # Dorado brillante
            )
            prompt_y = settings.VIRTUAL_HEIGHT // 2 + 35
        else:
            prompt_y = settings.VIRTUAL_HEIGHT // 2 + 20
