class QueuePriorityTool:

    PRIORITY_MAPPING = {

        "Emergency": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }

    @staticmethod
    def calculate_priority(
        urgency_level: str
    ):

        return (
            QueuePriorityTool
            .PRIORITY_MAPPING
            .get(
                urgency_level,
                4
            )
        )