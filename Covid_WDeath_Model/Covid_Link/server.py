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
        {"Label": "Immune to Covid", "Color": "#808080"},
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
        "Population",
        1000,
        10,
        5000,
        100,
        description="Choose how many agents to include in the model",
    ),
    
    "avg_node_degree": UserSettableParameter(
        "slider", 
        "Avg Close Contacts", 
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
        "Percentage of People Not Wearing Masks",
        0.9,
        0.0,
        1.0,
        0.1,
        description="If people are not wearing masks, the chance to spread covid is much higher.",
    ),
    "virus_check_frequency": UserSettableParameter(
        "slider",
        "Covid Test Frenquency",
        0.1,
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
    "gain_resistance_chance_from_infection": UserSettableParameter(
        "slider",
        "Gain Immunity Chance From Infecting Covid19",
        0.2,
        0.0,
        1.0,
        0.1,
        description="Probability that a recovered agent will become "
        "resistant to Covid 19 delta from infections",
    ),
    
    "double_vaccines_rate": UserSettableParameter(
	"slider",
	"Double Vaccines Rate",
	0.5,
	0.0,
	1.0,
	0.1,
	description="the rate of population receive double vaccines",
    ),
    
    "double_vaccines_efficiency": UserSettableParameter(
	"slider",
	"Double Vaccines Efficiency",
	0.6,
	0.0,
	1.0,
	0.1,
	description="the rate of susceptible population gain immunity after receiving two doses of vaccines",
    ),
    "death_rate": UserSettableParameter(
        "slider",
        "Death Rate",
        0.1,
        0.0,
        1.0,
        0.1,
        description="Probability that a infected agent will be dead ",
    ),
}

server = ModularServer(
    VirusOnNetwork, [network, MyTextElement(), chart], "COVID19 Delta Propagation", model_params
)
server.port = 8521
