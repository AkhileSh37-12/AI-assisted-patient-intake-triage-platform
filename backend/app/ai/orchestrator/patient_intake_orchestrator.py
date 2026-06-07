import asyncio
import json

from sqlalchemy.orm import Session

from app.ai.agents.intake_agent import (
    intake_agent
)

from app.ai.agents.triage_agent import (
    triage_agent
)

from app.ai.agents.routing_agent import (
    routing_agent
)

from app.ai.tools.triage_tool import (
    apply_triage_safety_rules
)

from app.services.patient_service import (
    get_or_create_patient_service
)

from app.schemas.patient_intake_schema import (
    PatientIntakeCreate
)

from app.services.patient_intake_service import (
    create_patient_intake
)

from datetime import date

from app.services.department_service import (
    get_department_by_name
)

from app.schemas.queue_entry_schema import (
    QueueEntryCreate
)

from app.services.queue_entry_service import (
    create_queue_entry_service,
    get_next_queue_number,
    get_next_queue_position
)

from app.services.doctor_assignment_service import (
    assign_doctor
)

from app.services.ai_processing_log_service import (
    log_ai_processing
)

from app.services.activity_log_service import (
    log_activity
)

class PatientIntakeOrchestrator:

    async def process_patient_intake(
        self,
        patient_input: str,
        db: Session
    ):

        # STEP 1 — Intake Agent

        intake_response = await asyncio.to_thread(
            intake_agent.run,
            patient_input
        )

        intake_result = json.loads(
            intake_response.content
        )

        # STEP 2 — Create Patient

        patient = get_or_create_patient_service(
            db,
            intake_result
        )

        symptoms = intake_result.get(
            "symptoms",
            ""
        )

        # STEP 3 — Parallel Agent Execution

        triage_task = asyncio.to_thread(
            triage_agent.run,
            f"""
            Patient symptoms:
            {symptoms}
            """
        )

        routing_task = asyncio.to_thread(
            routing_agent.run,
            f"""
            Patient symptoms:
            {symptoms}
            """
        )

        triage_response, routing_response = (
            await asyncio.gather(
                triage_task,
                routing_task
            )
        )

        # STEP 4 — Parse Agent Outputs

        triage_result = json.loads(
            triage_response.content
        )

        routing_result = json.loads(
            routing_response.content
        )

        # STEP 5 — Safety Validation

        safety_result = apply_triage_safety_rules(
            symptoms,
            triage_result["urgency_level"]
        )

        triage_result["urgency_level"] = (
            safety_result["urgency_level"]
        )

        triage_result["safety_override"] = (
            safety_result["override_applied"]
        )

        triage_result["safety_reason"] = (
            safety_result["reason"]
        )

        # STEP 6 — Create Intake Record

        intake_record = PatientIntakeCreate(

            patient_id=patient.patient_id,

            symptoms_text=symptoms,

            input_type="Text",

            created_by_user_id=1,

            ai_extracted_summary=symptoms,

            ai_urgency_level=triage_result.get(
                "urgency_level"
            ),

            ai_confidence_score=triage_result.get(
                "confidence_score"
            ),

            status="AI Processed"
        )

        priority_mapping = {

            "Emergency": 1,
            "High": 2,
            "Medium": 3,
            "Low": 4
        }

        priority_score = priority_mapping.get(
            triage_result.get(
                "urgency_level"
            ),
            4
        )

        saved_intake = create_patient_intake(
            db,
            intake_record
        )
        
        log_activity(

            db=db,

            user_id=1,

            activity_type="Patient Intake Created",

            entity_name="Patient Intake",

            entity_id=saved_intake.intake_id,

            activity_description=
            f"AI intake created for patient {patient.patient_id}"
        )
        
        log_ai_processing(
            db=db,
            intake_id=saved_intake.intake_id,
            ai_model_name="Gemini",
            processing_stage="Intake Agent",
            input_data=patient_input,
            output_data=json.dumps(intake_result)
        )
        
        log_ai_processing(
            db=db,
            intake_id=saved_intake.intake_id,
            ai_model_name="Gemini",
            processing_stage="Triage Agent",
            input_data=symptoms,
            output_data=json.dumps(triage_result),
            confidence_score=triage_result.get(
                "confidence_score"
            )
        )
        
        log_ai_processing(
            db=db,
            intake_id=saved_intake.intake_id,
            ai_model_name="Gemini",
            processing_stage="Routing Agent",
            input_data=symptoms,
            output_data=json.dumps(routing_result)
        )
        
        department_name = routing_result.get(
            "suggested_department"
        )

        department = get_department_by_name(
            db,
            department_name
        )
        
        assigned_doctor = assign_doctor(
            db,
            department.department_id
        )

        queue_number = get_next_queue_number(
            db
        )

        queue_position = get_next_queue_position(
            db,
            department.department_id
        )

        queue_entry = QueueEntryCreate(

            intake_id=saved_intake.intake_id,

            queue_date=date.today(),

            queue_number=queue_number,

            priority_score=priority_score,

            assigned_doctor_id=
            assigned_doctor.doctor_id,

            queue_position=queue_position,

            queue_status="Waiting",

            department_id=department.department_id
        )

        saved_queue = create_queue_entry_service(
            db,
            queue_entry
        )
        
        log_activity(

            db=db,

            user_id=1,

            activity_type="Queue Entry Created",

            entity_name="Queue Entry",

            entity_id=saved_queue.queue_id,

            activity_description=
            f"Patient assigned to doctor {assigned_doctor.doctor_id}"
        )
        # STEP 7 — Queue Priority



        # STEP 8 — Final Response

        return {

            "intake": intake_result,

            "triage": triage_result,

            "routing": routing_result,

            "queue": {
                "priority_score": priority_score
            }
        }