from fastapi import FastAPI

from app.db.database import engine, Base
from app.models.patient import Patient
from app.routes.patient_routes import router as patient_router
from app.models.department import Department
from app.routes.department_routes import router as department_router
from app.models.user import User
from app.routes.user_routes import router as user_router
from app.models.doctor import Doctor
from app.routes.doctor_routes import router as doctor_router
from app.models.role import Role
from app.routes.role_routes import router as role_router
from app.models.queue_entry import QueueEntry
from app.routes.queue_entry_routes import router as queue_entry_router
from app.models.patient_intake import PatientIntake
from app.routes.patient_intake_routes import router as patient_intake_router
from app.models.consultation import Consultation
from app.routes.consultation_routes import router as consultation_router
from app.models.ai_processing_log import AIProcessingLog
from app.routes.ai_processing_log_routes import router as ai_processing_log_router
from app.models.activity_log import ActivityLog
from app.routes.activity_log_routes import router as activity_log_router
from app.models.rag_knowledge_base import RAGKnowledgeBase
from app.routes.rag_knowledge_base_routes import router as rag_knowledge_base_router
from app.models.rag_retrieval_log import RAGRetrievalLog
from app.routes.rag_retrieval_log_routes import router as rag_retrieval_log_router
from app.routes.intake_ai_routes import router as intake_ai_router
from app.routes.rag_test_route import router as rag_test_router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.telemetry.tracing import tracer
Base.metadata.create_all(bind=engine)

app = FastAPI()

FastAPIInstrumentor.instrument_app(
    app
)

app.include_router(patient_router)
app.include_router(department_router)
app.include_router(user_router)
app.include_router(doctor_router)
app.include_router(role_router)
app.include_router(queue_entry_router)
app.include_router(patient_intake_router)
app.include_router(consultation_router)
app.include_router(ai_processing_log_router)
app.include_router(activity_log_router)
app.include_router(rag_knowledge_base_router)
app.include_router(rag_retrieval_log_router)
app.include_router(intake_ai_router)
app.include_router(rag_test_router)

@app.get("/")
def root():
    return {"message": "Backend Running"}