from app.models.ai_processing_log import (
    AIProcessingLog
)


class AILogger:

    @staticmethod
    def log(
        db,
        processing_stage,
        module_name,
        input_text,
        ai_response,
        processing_status="SUCCESS",
        error_message=None
    ):

        log = AIProcessingLog(

            processing_stage=processing_stage,

            module_name=module_name,

            input_text=input_text,

            ai_response=str(ai_response),

            processing_status=processing_status,

            error_message=error_message
        )

        db.add(log)

        db.commit()

        db.refresh(log)

        return log