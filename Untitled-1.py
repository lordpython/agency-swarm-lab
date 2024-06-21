# set openaiclint=python
from openai import OpenAI
import dotenv

# Load the environment variables
dotenv.load_dotenv()
# Create an instance of the OpenAI clinet
OpenAI = OpenAI()