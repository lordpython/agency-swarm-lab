from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

# Define your SERPER API credentials
api_key = os.getenv("SERPER_API_KEY")

class SERPERAPITool(BaseTool):
    """
    This tool interfaces with the SERPER API to enhance search capabilities and gather more comprehensive data.
    It handles authentication, makes requests to the SERPER API, and returns the relevant data.
    """

    # Define the fields with descriptions using Pydantic Field
    query: str = Field(
        ..., description="The search query to send to the SERPER API."
    )

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform the task.
        """
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Construct the request payload
        payload = {
            "q": self.query
        }

        # Make the request to the SERPER API
        response = requests.post(
            "https://api.serper.dev/search",
            headers=headers,
            json=payload
        )

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"

# Example usage:
# tool = SERPERAPITool(query="Artificial Intelligence")
# result = tool.run()
# print(result)