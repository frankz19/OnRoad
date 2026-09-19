import math
import pygame
from gale.physics.shapes import PolygonShape
from gale.physics.world import World
import settings


class Terrain:
    def __init__(self, world: World) -> None:
        self.segments = []
        # Línea base muy por debajo de la pantalla para cerrar los polígonos
        baseline = settings.VIRTUAL_HEIGHT + 600
        x = 0.0

        while x < settings.MAP_LENGTH:
            x0 = x
            x1 = min(x + settings.TERRAIN_STEP, settings.MAP_LENGTH)
            
            # Usamos la función global en settings para calcular la altura en X
            y0 = settings.terrain_height(x0)
            y1 = settings.terrain_height(x1)

            # Detectamos si es un pico muy alto para, opcionalmente, generar un hueco
            is_high_peak = y0 < 120 and y1 < 120

            # Evitamos huecos justo al inicio para que el jugador pueda arrancar
            safe_start_zone = x < settings.FLAT_START + settings.FLAT_TRANSITION + 100

            create_gap = (
                is_high_peak
                and not safe_start_zone
                and math.cos((x + settings.MAP_OFFSET) * 0.002) > 0.3
            )

            if not create_gap:
                # Si no hay hueco, creamos un polígono de colisión estático
                points = [(x0, y0), (x1, y1), (x1, baseline), (x0, baseline)]
                body = world.create_static_body(
                    0, 0, PolygonShape(points, friction=settings.TERRAIN_FRICTION)
                )
                body.user_data = "terrain"
                self.segments.append(points)

            x = x1

    def render(self, surface: pygame.Surface, offset_x: float, offset_y: float) -> None:
        # Se obtiene el ancho real de la superficie (considerando el zoom de la cámara)
        surface_width = surface.get_width()
        
        for points in self.segments:
            # Aplicamos el offset de la cámara a cada punto
            x0 = points[0][0] - offset_x
            y0 = points[0][1] - offset_y
            x1 = points[1][0] - offset_x
            y1 = points[1][1] - offset_y

            # Solo dibujamos si el segmento está visible en la superficie actual de la cámara
            if x0 < surface_width and x1 > 0:
                # Dibuja la línea principal del terreno (grosor 8)
                pygame.draw.line(surface, (139, 69, 19), (x0, y0), (x1, y1), 8)
                # Dibuja detalles debajo de la línea principal
                pygame.draw.line(surface, (60, 30, 10), (x0, y0 + 4), (x1, y1 + 4), 4)
                # Dibuja una línea de luz encima del terreno
                pygame.draw.line(surface, (170, 175, 180), (x0, y0 - 4), (x1, y1 - 4), 2)