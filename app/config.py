from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    whisper_model: str = "small"
    whisper_device: str = "auto"
