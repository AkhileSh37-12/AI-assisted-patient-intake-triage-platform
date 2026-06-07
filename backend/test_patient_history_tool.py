import app.models
from app.ai.tools.patient_history_tool import (
    get_patient_history
)
from app.models.patient import Patient
from app.db.database import (
    SessionLocal
)

db = SessionLocal()

history = get_patient_history(
    patient_id=18,
    db=db
)

print(history)

db.close()