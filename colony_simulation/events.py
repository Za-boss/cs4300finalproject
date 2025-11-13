from typing import TYPE_CHECKING, Callable
import random

if TYPE_CHECKING:
    from colony import Colony
    from building import Building

class Event:
    def __init__(
            self, 
            event_name: str,
            fire_event: Callable,
            fire_date: int | None = None,
            firing_likelihood: float | None = None,
            tick_effect: Callable | None = None
        ):
        self.event_name: str = event_name
        self.fire_event: Callable = fire_event
        self.fire_date: int | None = fire_date
        self.firing_likelihood: float | None = firing_likelihood
        self.tick_effect: Callable | None = tick_effect
        