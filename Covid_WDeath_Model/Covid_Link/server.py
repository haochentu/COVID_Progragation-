import math

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement
from .model import VirusOnNetwork, State, number_infected


def network_portrayal(G):
    # The model ensures there is always 1 agent per node

    def node_color(agent):
        return {State.INFECTED: "#FF0000", State.SUSCEPTIBLE: "#008000", State.DEAD: "#8B4500"}.get(
            agent.state, "#808080"
        )

    def edge_color(agent1, agent2):
        if State.RESISTANT in (agent1.state, agent2.state):
            return "#000000"
        return "#e8e8e8"

    def edge_width(agent1, agent2):
        if State.RESISTANT in (agent1.state, agent2.state):
            return 3
        return 2

    def get_agents(source, target):
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": "id: {}<br>state: {}".format(
                agents[0].unique_id, agents[0].state.name
            ),
        }
        for (_, agents) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": edge_color(*get_agents(source, target)),
            "width": edge_width(*get_agents(source, target)),
        }
        for (source, target) in G.edges
    ]

    return portrayal


network = NetworkModule(network_portrayal, 1000, 1000, library="d3")
chart = ChartModule(
    [
        {"Label": "Infected", "Color": "#FF0000"},
        {"Label": "Susceptible", "Color": "#008000"},
        {"Label": "Resistant", "Color": "#808080"},
        {"Label": "Dead", "Color": "#8B4500"},
        ]
)


class MyTextElement(TextElement):
    def render(self, model):
        ratio = model.resistant_susceptible_ratio()
        ratio_text = "&infin;" if ratio is math.inf else "{0:.2f}".format(ratio)
        infected_text = str(number_infected(model))

        return "Resistant/Susceptible Ratio: {}<br>Infected Remaining: {}".format(
            ratio_text, infected_text
        )


model_params = {
    "num_nodes": UserSettableParameter(
        "slider",
        "Number of agents",
        1000,
        10,
        5000,
        100,
        description="Choose how many agents to include in the model",
    ),
    "avg_node_degree": UserSettableParameter(
        "slider", 
        "Avg Node Degree", 
        5, 
        1, 
        12, 
        1, 
        description="Avg Node Degree"
    ),
    "initial_outbreak_size": UserSettableParameter(
        "slider",
        "Initial Outbreak Size",
        1,
        1,
        10,
        1,
        description="Initial Outbreak Size",
    ),
    "virus_spread_chance": UserSettableParameter(
        "slider",
        "Virus Spread Chance",
        0.6,
        0.0,
        1.0,
        0.1,
        description="Probability that susceptible neighbor will be infected",
    ),
    "virus_check_frequency": UserSettableParameter(
        "slider",
        "Virus Check Frequency",
        0.3,
        0.0,
        1.0,
        0.1,
        description="Frequency the nodes check whether they are infected by " "a virus",
    ),
    "recovery_chance": UserSettableParameter(
        "slider",
        "Recovery Chance",
        0.6,
        0.0,
        1.0,
        0.1,
        description="Probability that the virus will be removed",
    ),
    "gain_resistance_chance": UserSettableParameter(
        "slider",
        "Gain Resistance Chance",
        0.2,
        0.0,
        1.0,
        0.1,
        description="Probability that a recovered agent will become "
        "resistant to this virus in the future",
    ),
    "death_rate": UserSettableParameter(
        "slider",
        "Death Rate",
        0.2,
        0.0,
        1.0,
        0.1,
        description="Probability that a infected agent will be dead ",
    ),
}

server = ModularServer(
    VirusOnNetwork, [network, MyTextElement(), chart], "Virus Model", model_params
)
server.port = 8521