from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent

from agno.models.groq import Groq


from app.ai.prompts.routing_prompt import (
    ROUTING_PROMPT
)

routing_agent = Agent(

    name="Routing Agent",

    model=Groq(
        id="llama-3.1-8b-instant"
    ),


    instructions=ROUTING_PROMPT,

)