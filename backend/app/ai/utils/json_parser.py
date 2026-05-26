import json


class JSONParser:

    @staticmethod
    def parse(text: str):

        cleaned_text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            return json.loads(cleaned_text)

        except json.JSONDecodeError:

            raise Exception(
                "Invalid AI JSON response"
            )