import pygame

from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text

import settings
from src.World import World
from src.Motorcycle import Motorcycle


class OnRoadPlayState(BaseState):
    def enter(self, **params: dict):
        self.bike_index = params.get("bike_index", 0)
        self.paused = False

        self.world = World()
        # Instanciamos la moto en la parte izquierda de la pantalla
        self.motorcycle = Motorcycle(
            x=50, 
            y=settings.VIRTUAL_HEIGHT // 2, 
            bike_type=self.bike_index
        )
        
        # Puntuación basada en distancia
        self.score = 0
        self.timer = 0.0

        # --- GESTIÓN DE LA MÚSICA DE FONDO ---
        settings.stop_all_audio() # Detiene efectos o música anterior
        pygame.mixer.music.load(settings.ONROAD_MUSIC_PATH)
        pygame.mixer.music.set_volume(settings.ONROAD_MUSIC_VOLUME)
        pygame.mixer.music.play(loops=-1) # -1 significa bucle infinito

    def exit(self) -> None:
        # Detenemos la música al salir del estado (por ejemplo, al morir o pausar)
        pygame.mixer.music.stop()

    def update(self, dt: float) -> None:
        if self.paused:
            return

        self.world.update(dt)
        self.motorcycle.update(dt)
        
        # ¡Condición de Derrota! Si te quedas sin gasolina, se acaba.
        if self.motorcycle.fuel <= 0:
            self.state_machine.change("game_over", score=self.score)
        
        # Aumentamos la distancia recorrida (score) mientras jugamos
        self.timer += dt
        if self.timer >= 0.1: # Suma puntos constantemente
            self.score += 1
            self.timer = 0.0

        bike_rect = self.motorcycle.get_rect()

        # 1. Colisión con Items (Gasolina)
        for item in self.world.items:
            if bike_rect.colliderect(item.get_rect()):
                self.motorcycle.fuel = min(100.0, self.motorcycle.fuel + 15.0)
                item.active = False
                settings.SOUNDS["score"].play()

        # 2. Colisión con Obstáculos
        for obs in self.world.obstacles:
            if bike_rect.colliderect(obs.get_rect()):
                settings.SOUNDS["explosion"].play()
                self.state_machine.change("game_over", score=self.score)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.motorcycle.render(surface)
        
        render_text(
            surface,
            f"Distancia: {self.score}m",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH - 80,
            10,
            settings.COLOR_WHITE,
            center=True,
        )

        pygame.draw.rect(surface, (100, 0, 0), (10, 10, 100, 15))
        fuel_width = int((self.motorcycle.fuel / 100.0) * 100)
        fuel_color = (0, 200, 0) if self.motorcycle.fuel > 30 else (200, 200, 0)
        pygame.draw.rect(surface, fuel_color, (10, 10, fuel_width, 15))
        pygame.draw.rect(surface, settings.COLOR_WHITE, (10, 10, 100, 15), 2)
        
        render_text(
            surface,
            "Gasolina",
            settings.FONTS["medium"], 
            120,
            8,
            settings.COLOR_WHITE,
        )

        if self.paused:
            # Capa translúcida (ahora sí se verá bien el efecto semitransparente)
            overlay = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160)) # Negro con opacidad
            surface.blit(overlay, (0, 0))

            # Textos informativos de pausa
            render_text(
                surface,
                "JUEGO PAUSADO",
                settings.FONTS["large"] if "large" in settings.FONTS else settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2 - 40,
                settings.COLOR_WHITE,
                center=True,
            )

            render_text(
                surface,
                "Presiona 'P' para Continuar",
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2 + 10,
                (255, 255, 0), # Amarillo
                center=True,
            )

            render_text(
                surface,
                "Presiona ENTER para ir al Menu Principal",
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2 + 40,
                (200, 200, 200),
                center=True,
            )

    def on_input(self, input_id: str, input_data: InputData) -> None:

        if input_id == "pause" and input_data.pressed:
            self.paused = not self.paused  # Alterna entre True y False
            
            if self.paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        
        # Si está pausado, podemos permitir salir al menú principal con ENTER
        elif input_id == "confirm" and input_data.pressed and self.paused:
            self.state_machine.change("title")


        elif not self.paused:
            if input_id in ("up", "p1_accel", "p2_accel"):
                self.motorcycle.is_moving_up = input_data.pressed
            elif input_id in ("down", "p1_brake", "p2_brake"):
                self.motorcycle.is_moving_down = input_data.pressed
                
            if input_id in ("right", "p1_tilt_fwd", "p2_tilt_fwd"):
                self.motorcycle.is_accelerating = input_data.pressed
            elif input_id in ("left", "p1_tilt_back", "p2_tilt_back"):
                self.motorcycle.is_braking = input_data.pressed