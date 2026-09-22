from agent_learning.travel import TravelPlanner


def test_travel_planner_graph():
    planner = TravelPlanner(lambda _: {"destination": "Hangzhou"},
                            lambda city: {"city": city, "condition": "sunny"},
                            lambda _: [{"vendor": "demo", "price": 100}])
    state = planner.run("规划周末旅行")
    assert state.destination == "Hangzhou"
    assert state.itinerary and not state.errors

