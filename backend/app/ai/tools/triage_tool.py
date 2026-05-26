class TriageTool:

    HIGH_RISK_KEYWORDS = [
        "chest pain",
        "breathing difficulty",
        "shortness of breath",
        "unconscious",
        "severe bleeding",
        "stroke",
        "heart attack"
    ]

    @staticmethod
    def apply_safety_rules(
        symptoms: str,
        ai_urgency: str
    ):

        if not symptoms:
            return ai_urgency

        symptoms_lower = symptoms.lower()

        for keyword in (
            TriageTool.HIGH_RISK_KEYWORDS
        ):

            if keyword in symptoms_lower:

                if ai_urgency in [
                    "Low",
                    "Medium"
                ]:

                    return "High"

        return ai_urgency