import pygame

from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text


from src.HighScoreManager import HighScoreManager

import settings


class BikeSelectState(BaseState):
    def enter(self) -> None:

        self.selected_bike = 0
        self.unlocked_bikes = HighScoreManager.get_unlocked_bikes()
    
        self.bike_names = ["Socialista", "SBR", "Enduro", "Hyper Beast"]

        self.bike_info = [
            {"name": "Socialista", "desc": "Vieja, lenta pero fiel. Consume poco.", "req": 0},
            {"name": "SBR", "desc": "Moderna y equilibrada para la ciudad.", "req": 250},
            {"name": "Enduro", "desc": "Ágil, rápida y lista para el terreno duro.", "req": 500},
            {"name": "Hyper Beast", "desc": "Extrema. La más rápida... ¡Cuidado!", "req": 800}
        ]

    def on_input(self, input_id: str, input_data: InputData) -> None:

        if input_id in ("right", "p1_tilt_fwd", "p2_tilt_fwd") and input_data.pressed:
            self.selected_bike = min(3, self.selected_bike + 1)
        elif input_id in ("left", "p1_tilt_back", "p2_tilt_back") and input_data.pressed:
            self.selected_bike = max(0, self.selected_bike - 1)

        # Confirmar selección (Solo si está desbloqueada)
        if input_id == "confirm" and input_data.pressed:
            if self.selected_bike in self.unlocked_bikes:
                print(f"¡Iniciando carrera con la moto {self.selected_bike + 1}!")
                self.state_machine.change("play_onroad", bike_index=self.selected_bike)
            else:
                print("¡Esta moto está bloqueada! Necesitas más puntos.")

                

    def render(self, surface: pygame.Surface) -> None:

        surface.fill(settings.COLOR_BACKGROUND)

        background = settings.TEXTURES["garage"]
        background_rect = background.get_rect(
            # Mitad exacta de la pantalla en ambos ejes
            center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2) 
        )
        surface.blit(background, background_rect)

        render_text(
            surface,
            "Selecciona tu Nave",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 4,
            settings.COLOR_WHITE,
            center=True,
        )

        is_unlocked = self.selected_bike in self.unlocked_bikes

        bike_texture_key = f"bike_{self.selected_bike}"
        if bike_texture_key in settings.TEXTURES:
            bike_image = settings.TEXTURES[bike_texture_key]
        else:
            # Fallback por si acaso usa la genérica
            bike_image = settings.TEXTURES["bike"]

        scale_factor = 2 
        new_width = bike_image.get_width() * scale_factor
        new_height = bike_image.get_height() * scale_factor
        
        scaled_bike_image = pygame.transform.scale(bike_image, (new_width, new_height))

        # Dibujar la moto escalada y centrada en el garaje
        bike_rect = scaled_bike_image.get_rect(
            center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 - 10)
        )
        if not is_unlocked:
            # Creamos una copia para no alterar la textura original
            scaled_bike_image = scaled_bike_image.copy()
            # Multiplicamos sus canales de color por un tono gris oscuro (50, 50, 50)
            scaled_bike_image.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_MULT)

        bike_rect = scaled_bike_image.get_rect(center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 - 10))
        surface.blit(scaled_bike_image, bike_rect)

        # 4. Nombre y Estado (Bloqueada / Desbloqueada)
        current_bike_data = self.bike_info[self.selected_bike]
        render_text(surface, f"< {current_bike_data['name']} >", settings.FONTS["medium"], settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 + 50, settings.COLOR_WHITE, center=True)

        if is_unlocked:
            render_text(surface, current_bike_data["desc"], settings.FONTS["tiny"] if "tiny" in settings.FONTS else settings.FONTS["medium"], settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 + 80, (200, 200, 200), center=True)
            render_text(surface, "Presiona ENTER para correr", settings.FONTS["medium"], settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT - 30, settings.COLOR_WHITE, center=True)
        else:
            # Mensaje de requisitos con icono de candado simulado o texto rojo brillante
            req_text = f"🔒 BLOQUEADA (Requiere {current_bike_data['req']} pts)"
            render_text(surface, req_text, settings.FONTS["medium"], settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2 + 80, (255, 80, 80), center=True)
