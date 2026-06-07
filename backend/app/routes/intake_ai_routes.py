from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from app.schemas.intake_ai_schema import (
    IntakeAIRequest
)

from app.ai.orchestrator.patient_intake_orchestrator import (
    PatientIntakeOrchestrator
)

from sqlalchemy.orm import Session

from fastapi import Depends

from app.db.database import get_db

import tempfile
import os

from app.ai.voice.whisper_service import (
    WhisperService
)

router = APIRouter()

orchestrator = PatientIntakeOrchestrator()
whisper_service = WhisperService()


@router.post("/process")
async def process_intake(
    request: IntakeAIRequest
    , db: Session = Depends(get_db)
):


    result = await orchestrator.process_patient_intake(
        request.patient_input
        , db
    )

    return result

@router.post("/voice-process")
async def process_voice_intake(
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp_file:

        content = await audio_file.read()

        temp_file.write(content)

        temp_path = temp_file.name

    transcript = whisper_service.transcribe(
        temp_path
    )

    result = await orchestrator.process_patient_intake(
        transcript,
        db
    )

    os.remove(
        temp_path
    )

    return {

        "transcript": transcript,

        "result": result
    }