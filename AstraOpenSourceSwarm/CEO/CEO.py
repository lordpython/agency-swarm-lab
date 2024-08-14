from agency_swarm.agents import Agent


class CEO(Agent):
    def __init__(self):
        super().__init__(
            name="CEO",
            description="Manages communication between other agents",
            instructions="Please answer the question as best as you can, or communicate with the other agents as needed.",
            tools=[],
            # model="anthropic/claude-3-5-sonnet",
            model="claude-3-haiku-20240307",
        )
        
    def response_validator(self, message):
        return message
