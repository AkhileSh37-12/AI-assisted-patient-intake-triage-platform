from agno.agent import Agent

from agno.models.groq import Groq

from dotenv import load_dotenv

load_dotenv()

from app.ai.tools.triage_tool import (
    apply_triage_safety_rules
)

from app.ai.prompts.triage_prompt import (
    TRIAGE_PROMPT
)
print("LOADED NEW TRIAGE AGENT")

triage_agent = Agent(

    name="Triage Agent",

    model=Groq(
        id="llama-3.1-8b-instant"
    ),


    instructions=TRIAGE_PROMPT,

)