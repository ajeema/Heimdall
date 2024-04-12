class Environment:
    def __init__(self):
        self.agents = []
        self.resources = {}
        self.time = 0

    def register_agent(self, agent):
        """Register an agent to the environment."""
        self.agents.append(agent)
        print(f"Agent {agent.name} registered to the environment.")

    def update_resources(self, resource_key, amount):
        """Update the amount of a specific resource."""
        if resource_key in self.resources:
            self.resources[resource_key] += amount
        else:
            self.resources[resource_key] = amount

    def step(self):
        """Advance the simulation by one time step."""
        self.time += 1
        for agent in self.agents:
            agent.act(self)
        print(f"Environment advanced to time {self.time}.")

    def get_resource(self, resource_key):
        """Retrieve the amount of a specific resource."""
        return self.resources.get(resource_key, 0)
