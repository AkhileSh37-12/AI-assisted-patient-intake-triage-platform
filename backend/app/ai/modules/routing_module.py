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

from app.ai.tools.department_validation_tool import (
    DepartmentValidationTool
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

        is_valid = (
            DepartmentValidationTool.validate(
                department
            )
        )

        if not is_valid:

            parsed_response[
                "suggested_department"
            ] = "General Medicine"

        return parsed_response