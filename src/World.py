import pygame
import random
import settings
from src.GameObjects import GameObject


class World:
    def __init__(self) -> None:
        self.background_x: float = 0.0
        self.ground_x: float = 0.0
        
        
        # Obstáculos (Piedras/Troncos) y Recursos (Gasolina)
        self.obstacles = []
        self.items = []
        self.spawn_timer = 0.0
        self.next_spawn_time = random.uniform(0.8, 2.0)
        self.obstacle_index = 0
        
        # Temporizador de dificultad y control de posición anterior
        self.difficulty_timer = 0.0
        self.last_spawn_y = 0.0
        

    def update(self, dt: float) -> None:

        try: 
            self.difficulty_timer += dt
            current_scroll_speed = settings.MAIN_SCROLL_SPEED + min(200, self.difficulty_timer * 10.0)
            # 1. Movimiento cíclico del fondo
            bg_width = settings.TEXTURES["background"].get_width()
            self.background_x -= settings.BACK_SCROLL_SPEED * dt
            if self.background_x <= -bg_width:
                self.background_x += bg_width

            ground_width = settings.TEXTURES["ground"].get_width()
            self.ground_x -= current_scroll_speed * dt
            if self.ground_x <= -ground_width:
                self.ground_x += ground_width

            #Generacion de Objetos Aleatorios
            self.spawn_timer += dt
            if self.spawn_timer > self.next_spawn_time:
                self.spawn_timer = 0.0
                
                min_y = settings.TRACK_TOP + 5
                max_y = settings.VIRTUAL_HEIGHT - 40 
                spawn_y = random.randint(min_y, max_y)
                while abs(spawn_y - self.last_spawn_y) < 45: # Al menos 45 píxeles de distancia vertical con el anterior
                    spawn_y = random.randint(min_y, max_y)
                self.last_spawn_y = spawn_y

                spawn_x = settings.VIRTUAL_WIDTH + 50
                
                if random.random() < 0.7: 
                    variant = self.obstacle_index % 4
                    self.obstacles.append(GameObject(spawn_x, spawn_y, "obstacle", variant=variant))
                    self.obstacle_index += 1
                else:
                    self.items.append(GameObject(spawn_x, spawn_y, "fuel"))


                reduction_factor = min(1.2, self.difficulty_timer * 0.03)
                self.next_spawn_time = max(0.5, random.uniform(1.5, 2.5) - reduction_factor)

            for obs in self.obstacles:
                obs.x -= current_scroll_speed * dt # ¡Aquí estaba el detalle! Ahora sí usan la velocidad acelerada
                if obs.x + obs.width < 0:
                    obs.active = False
            for item in self.items:
                item.x -= current_scroll_speed * dt
                if item.x + item.width < 0:
                    item.active = False

            self.obstacles = [o for o in self.obstacles if o.active]
            self.items = [i for i in self.items if i.active]
        except Exception as e:
                    print(f"¡ERROR ATRAPADO EN WORLD UPDATE: {e}")


    def render(self, surface: pygame.Surface) -> None:
        bg_texture = settings.TEXTURES["background"]
        bg_width = bg_texture.get_width()
        
        surface.blit(bg_texture, (round(self.background_x), 0))
        surface.blit(bg_texture, (round(self.background_x) + bg_width - 1, 0))

        ground_texture = settings.TEXTURES["ground"]
        ground_width = ground_texture.get_width()
        
        surface.blit(ground_texture, (round(self.ground_x), settings.TRACK_TOP))
        surface.blit(ground_texture, (round(self.ground_x) + ground_width - 1, settings.TRACK_TOP))

        for item in self.items:
            item.render(surface)
        for obs in self.obstacles:
            obs.render(surface)
