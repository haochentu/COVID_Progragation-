from .model import MoneyModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa import Agent, Model
from .agent import MoneyAgent

def agent_portrayal(agent):
    portrayal = {"Shape": "Circle", "Filled": "true", "r": 0.5}
    if agent.wealth > 0:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(MoneyModel,
                       [grid],
                       "Money Model",
                       {"N":100, "width":10,"height":10})
server.port = 8521

