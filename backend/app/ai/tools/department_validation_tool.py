class DepartmentValidationTool:

    ALLOWED_DEPARTMENTS = [

        "Emergency",
        "General Medicine",
        "Cardiology",
        "Neurology",
        "Orthopedics",
        "ENT",
        "Dermatology",
        "Pediatrics",
        "Pulmonology",
        "Gastroenterology",
        "Nephrology",
        "Psychiatry",
        "Oncology",
        "Gynecology",
        "Urology",
        "Endocrinology"
    ]

    @staticmethod
    def validate(
        department: str
    ):

        return (
            department
            in
            DepartmentValidationTool
            .ALLOWED_DEPARTMENTS
        )