import pygame
import settings

class GameObject:
    def __init__(self, x: float, y: float, type_key: str, variant: int = 0):
        self.x = x
        self.y = y

        self.type_key = type_key
        self.variant = variant


        if type_key == "obstacle":
            self.image = settings.FRAMES["obstacles"][variant]
        else:
            self.image = settings.TEXTURES[type_key]

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.active = True

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        self.x -= settings.MAIN_SCROLL_SPEED * dt

        if self.x + self.width < 0:
            self.active = False

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, (round(self.x), round(self.y)))