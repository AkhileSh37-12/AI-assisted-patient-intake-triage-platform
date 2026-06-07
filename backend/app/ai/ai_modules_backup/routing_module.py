from app.ai.gemini_client import model

from app.ai.prompts.routing_prompt import (
    ROUTING_PROMPT
)

from app.ai.utils.json_parser import (
    JSONParser
)

from app.ai.utils.retry_handler import (
    RetryHandler
)


class RoutingModule:

    async def process(
        self,
        symptoms: str
    ):

        prompt = f"""
        {ROUTING_PROMPT}

        PATIENT SYMPTOMS:
        {symptoms}
        """

        async def generate():

            return model.generate_content(
                prompt
        )

        response = await RetryHandler.retry(
            generate
        )

        raw_text = response.text.strip()

        parsed_response = JSONParser.parse(
            raw_text
        )
        
        department = parsed_response.get(
            "suggested_department"
        )

        return parsed_response