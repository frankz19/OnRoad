import pygame

import settings


class Motorcycle:
    def __init__(self, x, y, bike_type):
        self.x = x
        self.y = y
        self.bike_type = bike_type 
        
        # --- Variables de dimensión (¡Vitales para evitar el crash!) ---
        self.width = settings.BIKE_WIDTH
        self.height = settings.BIKE_HEIGHT
        
        # Físicas y Estadísticas Base
        self.speed = 0
        self.dx = 0 # Movimiento horizontal (acelerar/frenar)
        self.dy = 0 # Movimiento vertical (cambio de carril)
        self.max_speed_x = 250       # Velocidad máxima hacia adelante
        self.accel_x = 500           # Aceleración horizontal
        
        self.max_speed_y = 120       # Velocidad máxima de cambio de carril (reducida)
        self.accel_y = 400           # Agilidad lateral (reducida)
        
        self.friction = 300

        self.is_accelerating = False
        self.is_braking = False
        self.is_moving_up = False
        self.is_moving_down = False
        
        self.fuel = 100.0
        self.fuel_drain_rate = 2.0


        self.tire_health = 100
        texture_key = f"bike_{self.bike_type}"
        if texture_key in settings.TEXTURES:
            self.image = settings.TEXTURES[texture_key]
        else:
            self.image = settings.TEXTURES["bike"]


    def get_rect(self) -> pygame.Rect:
        
        rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)    
        rect.y += 20
        
        return rect


    def update(self, dt: float) -> None:

        if self.is_accelerating:
            self.fuel -= (self.fuel_drain_rate * 2) * dt
        else:
            self.fuel -= self.fuel_drain_rate * dt
            
        self.fuel = max(0.0, self.fuel)



        if self.is_accelerating:
            self.dx += self.accel_x * dt
        elif self.is_braking:
            self.dx -= self.accel_x * 1.5 * dt
        else:
            if self.dx > 0:
                self.dx = max(0, self.dx - self.friction * dt)
            elif self.dx < 0:
                self.dx = min(0, self.dx + self.friction * dt)

        self.dx = max(-self.max_speed_x, min(self.dx, self.max_speed_x))

        # 3. Lógica Eje Y (Ahora usa accel_y y max_speed_y)
        if self.is_moving_up:
            self.dy -= self.accel_y * dt
        elif self.is_moving_down:
            self.dy += self.accel_y * dt
        else:
            if self.dy > 0:
                self.dy = max(0, self.dy - self.friction * dt)
            elif self.dy < 0:
                self.dy = min(0, self.dy + self.friction * dt)
                
        self.dy = max(-self.max_speed_y, min(self.dy, self.max_speed_y))
        

        self.x += self.dx * dt
        self.y += self.dy * dt
        
        self.x = max(0, min(self.x, settings.VIRTUAL_WIDTH - self.width))
        
        offset_y = 20
        
        min_y = settings.TRACK_TOP - offset_y
        max_y = settings.VIRTUAL_HEIGHT - self.height - offset_y
        
        self.y = max(min_y, min(self.y, max_y))

    def render(self, surface: pygame.Surface) -> None:

        surface.blit(self.image, (round(self.x), round(self.y)))