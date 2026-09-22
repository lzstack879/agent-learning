from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class TravelState:
    request: str
    destination: str | None = None
    weather: dict | None = None
    prices: list[dict] = field(default_factory=list)
    itinerary: str | None = None
    errors: list[str] = field(default_factory=list)


class TravelPlanner:
    """A framework-free graph equivalent; replace nodes with LangGraph StateGraph in week 4."""
    def __init__(self, search: Callable[[str], dict], weather: Callable[[str], dict], prices: Callable[[str], list[dict]]) -> None:
        self.search, self.weather, self.prices = search, weather, prices

    def run(self, request: str) -> TravelState:
        state = TravelState(request=request)
        try:
            state.destination = self.search(request).get("destination")
            if not state.destination:
                state.errors.append("destination not found")
                return state
            state.weather = self.weather(state.destination)
            state.prices = self.prices(state.destination)
            state.itinerary = self._itinerary(state)
        except Exception as exc:
            state.errors.append(str(exc))
        return state

    @staticmethod
    def _itinerary(state: TravelState) -> str:
        return (f"{state.destination} trip: weather={state.weather}; "
                f"options={len(state.prices)}; plan morning sightseeing and evening local food.")

