from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

# Define your LinkedIn API credentials
api_key = os.getenv("LINKEDIN_API_KEY")
api_secret = os.getenv("LINKEDIN_API_SECRET")
access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")

class LinkedInAPITool(BaseTool):
    """
    This tool interfaces with the LinkedIn API to search for posts based on specified keywords, industries, or profiles.
    It handles authentication, makes requests to the LinkedIn API, and returns the relevant data.
    """

    # Define the fields with descriptions using Pydantic Field
    keywords: str = Field(
        ..., description="Keywords to search for in LinkedIn posts."
    )
    industries: str = Field(
        None, description="Industries to filter the LinkedIn posts."
    )
    profiles: str = Field(
        None, description="Profiles to filter the LinkedIn posts."
    )

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform the task.
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Construct the search query
        query = f"keywords={self.keywords}"
        if self.industries:
            query += f"&industries={self.industries}"
        if self.profiles:
            query += f"&profiles={self.profiles}"

        # Make the request to the LinkedIn API
        response = requests.get(
            f"https://api.linkedin.com/v2/posts?{query}",
            headers=headers
        )

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"

# Example usage:
# tool = LinkedInAPITool(keywords="AI", industries="Technology", profiles="John Doe")
# result = tool.run()
# print(result)