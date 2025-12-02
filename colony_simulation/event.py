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
            fire_dates: tuple[int, ...] | None = (),
            firing_likelihood: float | None = None,
            tick_effect: Callable | None = None,
            fire_count: int = 1
        ):

        self.event_name: str = event_name
        self.fire_event: Callable = fire_event
        self.fire_dates: tuple[int, ...] | None = fire_dates
        self.firing_likelihood: float | None = firing_likelihood
        self.tick_effect: Callable | None = tick_effect
        self.fire_count = fire_count

    def __repr__(self) -> str:
        if self.fire_dates:
            return f"Event Name: {self.event_name} | Firing Dates: {self.fire_dates}"
        elif self.firing_likelihood:
            return f"Event Name: {self.event_name} | Firing Likelihood: {self.firing_likelihood} | Fire Count: {self.fire_count}"
        return f"Event Name: {self.event_name}"