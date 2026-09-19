import pygame
import settings

from gale.game import Game
from gale.state import StateMachine
from gale.input_handler import InputData

from src import states


class OnRoad(Game):
    def init(self) -> None:
        self.state_machine = StateMachine(
            {
                "high_score": states.HighScoreState,
                "enter_high_score": states.EnterHighScoreState,
                "game_over": states.GameOverState,
                "bike_select": states.BikeSelectState,
                "play_onroad": states.OnRoadPlayState,
                "play_racing": states.RacingPlayState,
                "stats_racing": states.StatsState,
                "title": states.TitleScreenState,
            }
        )
        # Ya NO cargamos la música aquí. Se carga en TitleScreenState.enter()
        # cada vez que se entra al título. Así, cuando el jugador muere y
        # vuelve al menú, la música del título arranca correctamente.
        self.state_machine.change("title")

    def update(self, dt: float) -> None:
        self.state_machine.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.state_machine.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "quit" and input_data.pressed:
            self.quit()
        else:
            self.state_machine.on_input(input_id, input_data)