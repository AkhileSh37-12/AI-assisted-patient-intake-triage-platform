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

from app.ai.rag.retrieval_service import (
    retrieve_relevant_chunks
)

from app.models.rag_retrieval_log import (
    RAGRetrievalLog
)

from app.telemetry.tracing import (
    tracer,
    logger
)

from app.models.user import User
 
class PatientIntakeOrchestrator:

    async def process_patient_intake(
        self,
        patient_input: str,
        db: Session
    ):

        # STEP 1 — Intake Agent

        with tracer.start_as_current_span(
            "intake_agent"
        ) as span:

            span.add_event(
                "Patient intake started"
            )
            
            logger.info(
                "AI Intake Agent started"
            )

            intake_response = await asyncio.to_thread(
                intake_agent.run,
                patient_input
            )
            
            logger.info(
                "Intake agent response received"
            )

            intake_result = json.loads(
                intake_response.content
            )

            span.set_attribute(
                "patient.name",
                str(
                    intake_result.get(
                        "full_name",
                        ""
                    )
                )
            )

            span.set_attribute(
                "patient.age",
                int(
                    intake_result.get(
                        "age",
                        0
                    )
                )
            )

            span.set_attribute(
                "patient.phone",
                str(
                    intake_result.get(
                        "phone_number",
                        ""
                    )
                )
            )

            span.set_attribute(
                "patient.symptoms",
                str(
                    intake_result.get(
                        "symptoms",
                        ""
                    )
                )
            )

            span.add_event(
                "Patient intake completed"
            )
            
            logger.info(
                f"Patient extracted: {intake_result.get('full_name')}"
            )

        # STEP 2 — Create Patient

        with tracer.start_as_current_span(
            "patient_creation"
        ) as span:

            patient = get_or_create_patient_service(
                db,
                intake_result
            )
            
            symptoms = intake_result.get(
                        "symptoms",
                        ""
                    )
            
            span.set_attribute(
                "patient.id",
                patient.patient_id
            )

            span.add_event(
                "Patient record created"
            )
            
            logger.info(
                f"Patient record created: patient_id={patient.patient_id}"
            )

        
        with tracer.start_as_current_span(
            "rag_retrieval"
        ) as span:

            span.set_attribute(
                "symptoms",
                symptoms
            )

            span.add_event(
                "RAG retrieval started"
            )
            
            logger.info(
                f"RAG retrieval started for symptoms={symptoms}"
            )

            rag_chunks = retrieve_relevant_chunks(
                db=db,
                query=symptoms,
                top_k=3
            )
            
            rag_context = "\n\n".join(

                        [
                            f"""
                            Title: {chunk.title}

                            Content: {chunk.content}
                            """

                            for chunk in rag_chunks
                        ]
                    )

            span.set_attribute(
                "rag.documents_found",
                len(rag_chunks)
            )

            if len(rag_chunks) > 0:

                span.set_attribute(
                    "rag.top_document",
                    rag_chunks[0].title
                )

                span.set_attribute(
                    "rag.top_specialty",
                    rag_chunks[0].medical_specialty
                )
                
                logger.info(
                    f"Top RAG document: {rag_chunks[0].title}"
                )

            span.add_event(
                "RAG retrieval completed"
            )
            
            logger.info(
                f"RAG retrieved {len(rag_chunks)} documents"
            )
            
            for chunk in rag_chunks:

                logger.info(
                    f"RAG Match: {chunk.title}"
                )


        # STEP 3 — Parallel Agent Execution

        triage_task = asyncio.to_thread(
            triage_agent.run,
            f"""
            Patient symptoms:
            {symptoms}

            Relevant medical knowledge:

            {rag_context}
            """
        )

        routing_task = asyncio.to_thread(
            routing_agent.run,
            f"""
            Patient symptoms:
            {symptoms}

            Relevant medical knowledge:

            {rag_context}
            """
        )

        with tracer.start_as_current_span(
            "triage_and_routing"
        ) as span:

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
        
            span.set_attribute(
                "triage.urgency",
                str(
                    triage_result.get(
                        "urgency_level",
                        ""
                    )
                )
            )

            span.set_attribute(
                "triage.confidence",
                float(
                    triage_result.get(
                        "confidence_score",
                        0
                    )
                )
            )

            span.set_attribute(
                "routing.department",
                str(
                    routing_result.get(
                        "suggested_department",
                        ""
                    )
                )
            )

            span.add_event(
                "AI triage completed"
            )
            
            logger.info(
                f"Triage completed: urgency={triage_result.get('urgency_level')}"
            )

            span.add_event(
                "Department routing completed"
            )
            
            logger.info(
                f"Department routed: {routing_result.get('suggested_department')}"
            )

        # STEP 5 — Safety Validation

        with tracer.start_as_current_span(
            "safety_validation"
        ) as span:

            safety_result = apply_triage_safety_rules(
                symptoms,
                triage_result["urgency_level"]
            )
            
            span.set_attribute(
                "safety.override",
                bool(
                    safety_result[
                        "override_applied"
                    ]
                )
            )

            span.set_attribute(
                "safety.final_urgency",
                str(
                    safety_result[
                        "urgency_level"
                    ]
                )
            )

            span.set_attribute(
                "safety.reason",
                str(
                    safety_result[
                        "reason"
                    ]
                )
            )

            span.add_event(
                "Safety validation completed"
            )
            
            logger.info(
                f"Safety validation completed: "
                f"override={safety_result['override_applied']}, "
                f"final_urgency={safety_result['urgency_level']}"
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

        department_name = routing_result.get(
            "suggested_department"
        )

        department = get_department_by_name(
            db,
            department_name
        )

        # STEP 6 — Create Intake Record

        intake_record = PatientIntakeCreate(

            patient_id=patient.patient_id,

            symptoms_text=symptoms,

            input_type="Text",

            created_by_user_id=1,

            ai_extracted_summary=symptoms,
            
            suggested_department_id=department.department_id,
            
            ai_urgency_level=triage_result.get(
                "urgency_level"
            ),

            ai_confidence_score=triage_result.get(
                "confidence_score"
            ),

            staff_verified=False,
            status="Pending",
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

        with tracer.start_as_current_span(
            "save_intake"
        ) as span:

            span.set_attribute(
                "urgency_level",
                triage_result.get(
                    "urgency_level"
                )
            )

            saved_intake = create_patient_intake(
                db,
                intake_record
            )
            
            span.set_attribute(
                "workflow.id",
                f"intake_{saved_intake.intake_id}"
            )
            
            workflow_intake_id = (
                saved_intake.intake_id
            )
            
            span.set_attribute(
                "intake.id",
                saved_intake.intake_id
            )

            span.set_attribute(
                "patient.id",
                patient.patient_id
            )
            
            span.add_event(
                "Patient intake saved"
            )
            
            logger.info(
                f"Intake saved: intake_id={saved_intake.intake_id}"
            )
            
        with tracer.start_as_current_span(
            "retrieval_logging"
        ) as span:
            
            for rank, chunk in enumerate(
                rag_chunks,
                start=1
            ):

                retrieval_log = RAGRetrievalLog(

                    intake_id=saved_intake.intake_id,

                    knowledge_id=chunk.knowledge_id,

                    retrieval_rank=rank,

                    similarity_score=None
                )

                db.add(retrieval_log)

            db.commit()
            span.set_attribute(
                "workflow.id",
                f"intake_{saved_intake.intake_id}"
            )
            
            span.set_attribute(
                "retrieval.count",
                len(rag_chunks)
            )
            
            for index, chunk in enumerate(rag_chunks):

                span.set_attribute(
                    f"retrieval.doc_{index+1}",
                    chunk.title
                )

                span.set_attribute(
                    f"retrieval.specialty_{index+1}",
                    chunk.medical_specialty
                )

            span.set_attribute(
                "intake.id",
                saved_intake.intake_id
            )

            span.add_event(
                "Retrieval logs saved"
            )
            
            logger.info(
                f"RAG retrieval logs saved for intake={saved_intake.intake_id}"
            )
        
        
        with tracer.start_as_current_span(
            "ai_processing_logs"
        ) as span:

            span.set_attribute(
                "intake.id",
                workflow_intake_id
            )

            span.set_attribute(
                "patient.id",
                patient.patient_id
            )
            span.set_attribute(
                "workflow.id",
                f"intake_{saved_intake.intake_id}"
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
            
            logger.info(
                f"AI processing logs saved for intake={saved_intake.intake_id}"
            )
            
        # STEP 7 — Queue Priority



        # STEP 8 — Final Response

        return {
            "intake": intake_result,
            "triage": triage_result,
            "routing": routing_result,
            "rag_context": [
                {
                    "title": chunk.title,
                    "specialty": chunk.medical_specialty
                }
                for chunk in rag_chunks
            ],
            "verification_status": {
                "staff_verified": False,
                "status": "Pending"
            }
        }