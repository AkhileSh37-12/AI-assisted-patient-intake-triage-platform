from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.models.groq import Groq

from app.ai.prompts.intake_extraction_prompt import (
    INTAKE_EXTRACTION_PROMPT
)

intake_agent = Agent(

    name="Intake Agent",

    model=Groq(
        id="llama-3.1-8b-instant"
    ),

    instructions=INTAKE_EXTRACTION_PROMPT,
)