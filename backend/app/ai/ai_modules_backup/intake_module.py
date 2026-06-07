import json

from app.ai.groq_client import client

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

            response = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2
            )

            return response

        response = await RetryHandler.retry(
            generate
        )

        raw_text = (
            response
            .choices[0]
            .message
            .content
        )

        parsed_response = (
            JSONParser.parse(
                raw_text
            )
        )

        return parsed_response