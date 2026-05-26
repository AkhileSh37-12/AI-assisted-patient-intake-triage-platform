import asyncio

from app.ai.modules.intake_module import (
    IntakeModule
)

from app.ai.modules.triage_module import (
    TriageModule
)

from app.ai.modules.routing_module import (
    RoutingModule
)

from app.ai.tools.queue_priority_tool import (
    QueuePriorityTool
)

from app.services.patient_service import (
    create_patient_service
)

from sqlalchemy.orm import Session

class PatientIntakeOrchestrator:

    def __init__(self):

        self.intake_module = IntakeModule()

        self.triage_module = TriageModule()

        self.routing_module = RoutingModule()

    async def process_patient_intake(
        self,
        patient_input: str
        , db: Session
    ):

        # STEP 1 — Intake Extraction

        intake_result = await self.intake_module.process(
            patient_input
        )
        
        patient = (
            create_patient_service(
                db,
                intake_result
            )
        )

        symptoms = intake_result.get(
            "symptoms",
            ""
        )

        # STEP 2 — Parallel Execution

        triage_task = (
            self.triage_module.process(
                symptoms
            )
        )

        routing_task = (
            self.routing_module.process(
                symptoms
            )
        )

        triage_result, routing_result = (
            await asyncio.gather(
                triage_task,
                routing_task
            )
        )
        
        priority_score = (
            QueuePriorityTool.calculate_priority(
                triage_result.get(
                "urgency_level"
                )
            )
        )

        # STEP 3 — Final Response

        return {
            "intake": intake_result,
            "triage": triage_result,
            "routing": routing_result,
            "queue": {
                "priority_score": priority_score
            }
        }