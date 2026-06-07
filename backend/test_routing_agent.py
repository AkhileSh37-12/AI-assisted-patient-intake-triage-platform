from app.ai.agents.routing_agent import (
    routing_agent
)

response = routing_agent.run(

    """
    Patient has severe skin rash
    and hair loss.
    """
)

print(
    response.content
    .replace("</function>", "")
)