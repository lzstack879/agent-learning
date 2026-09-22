from __future__ import annotations

import asyncio
from datetime import date
from typing import Any

from pydantic import BaseModel, Field

from .core import Tool


class WeatherArgs(BaseModel):
    city: str = Field(min_length=1, max_length=80)


class ExchangeArgs(BaseModel):
    base: str = Field(min_length=3, max_length=3)
    quote: str = Field(min_length=3, max_length=3)
    amount: float = Field(gt=0)


class TodoArgs(BaseModel):
    action: str = Field(pattern="^(add|list|done)$")
    title: str | None = Field(default=None, max_length=200)


class CalendarArgs(BaseModel):
    action: str = Field(pattern="^(list|add)$")
    day: date | None = None
    title: str | None = Field(default=None, max_length=200)


class SearchArgs(BaseModel):
    query: str = Field(min_length=2, max_length=200)


_todos: list[dict[str, Any]] = []
_events: list[dict[str, Any]] = []


async def weather(city: str) -> dict[str, Any]:
    await asyncio.sleep(0)
    return {"city": city, "condition": "sunny", "temperature_c": 22}


async def exchange(base: str, quote: str, amount: float) -> dict[str, Any]:
    rates = {("USD", "CNY"): 7.2, ("CNY", "USD"): 1 / 7.2, ("EUR", "USD"): 1.08}
    rate = rates.get((base.upper(), quote.upper()))
    if rate is None:
        raise ValueError("unsupported currency pair")
    return {"base": base.upper(), "quote": quote.upper(), "amount": amount, "result": amount * rate}


async def todo(action: str, title: str | None = None) -> dict[str, Any]:
    if action == "add":
        if not title:
            raise ValueError("title is required for add")
        _todos.append({"title": title, "done": False})
    elif action == "done":
        if not title:
            raise ValueError("title is required for done")
        for item in _todos:
            if item["title"] == title:
                item["done"] = True
    return {"items": list(_todos)}


async def calendar(action: str, day: date | None = None, title: str | None = None) -> dict[str, Any]:
    if action == "add":
        if not day or not title:
            raise ValueError("day and title are required for add")
        _events.append({"day": day.isoformat(), "title": title})
    return {"events": list(_events)}


async def search(query: str) -> dict[str, Any]:
    await asyncio.sleep(0)
    return {"query": query, "results": [f"Demo result for: {query}"]}


def default_tools() -> list[Tool]:
    return [
        Tool("weather", "Get current weather", WeatherArgs, weather),
        Tool("exchange", "Convert currencies", ExchangeArgs, exchange),
        Tool("todo", "Manage todos", TodoArgs, todo),
        Tool("calendar", "Manage calendar events", CalendarArgs, calendar),
        Tool("search", "Search the web", SearchArgs, search),
    ]

