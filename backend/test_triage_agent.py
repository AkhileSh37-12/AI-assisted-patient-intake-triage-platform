
from app.ai.agents.triage_agent import (
    triage_agent
)

response = triage_agent.run(

    """
    Patient has chest pain
    and breathing difficulty.
    AI urgency is low.
    """
)

print(
    response.content
    .replace("</function>", "")
)