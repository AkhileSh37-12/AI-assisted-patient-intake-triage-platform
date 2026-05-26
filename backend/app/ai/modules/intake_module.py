import json

from app.ai.gemini_client import model

from app.ai.prompts.intake_extraction_prompt import (
    INTAKE_EXTRACTION_PROMPT
)

from app.ai.utils.json_parser import (
    JSONParser
)

from app.ai.utils.retry_handler import (
    RetryHandler
)

class IntakeModule:

    async def process(
        self,
        patient_input: str
    ):

        prompt = f"""
        {INTAKE_EXTRACTION_PROMPT}

        PATIENT INPUT:
        {patient_input}
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

        return parsed_response