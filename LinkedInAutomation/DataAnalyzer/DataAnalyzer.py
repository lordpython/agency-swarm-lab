from agency_swarm.agents import Agent
from agency_swarm.tools import CodeInterpreter

class DataAnalyzer(Agent):
    def __init__(self):
        super().__init__(
            name="DataAnalyzer",
            description="Analyzes the scraped data to extract meaningful insights and filter relevant posts.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CodeInterpreter],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
        
    def response_validator(self, message):
        print(message)
