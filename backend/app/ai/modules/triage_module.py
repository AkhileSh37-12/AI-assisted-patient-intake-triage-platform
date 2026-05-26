from app.ai.gemini_client import model

from app.ai.prompts.triage_prompt import (
    TRIAGE_PROMPT
)

from app.ai.tools.triage_tool import (
    TriageTool
)

from app.ai.utils.json_parser import (
    JSONParser
)

from app.ai.utils.retry_handler import (
    RetryHandler
)

class TriageModule:

    def __init__(self):

        self.triage_tool = TriageTool()

    async def process(
        self,
        symptoms: str
    ):

        prompt = f"""
        {TRIAGE_PROMPT}

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

        ai_urgency = parsed_response.get(
            "urgency_level",
            "Low"
        )

        validated_urgency = (
            self.triage_tool.apply_safety_rules(
                symptoms,
                ai_urgency
            )
        )

        parsed_response[
            "urgency_level"
        ] = validated_urgency

        return parsed_response