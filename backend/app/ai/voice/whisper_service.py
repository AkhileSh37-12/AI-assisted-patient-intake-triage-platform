from faster_whisper import WhisperModel


class WhisperService:

    def __init__(self):

        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    def transcribe(
        self,
        audio_path: str
    ):

        segments, info = (
            self.model.transcribe(
                audio_path
            )
        )

        full_text = ""

        for segment in segments:

            full_text += (
                segment.text + " "
            )

        return full_text.strip()