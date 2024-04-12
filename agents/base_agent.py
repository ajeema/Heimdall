class Agent:
    def __init__(self, agent_id, environment):
        self.agent_id = agent_id
        self.environment = environment

    def act(self):
        raise NotImplementedError

    def communicate(self, message, recipient_id):
        self.environment.send_message(self.agent_id, recipient_id, message)

    def receive(self, message):
        print(f"Agent {self.agent_id} received: {message}")

