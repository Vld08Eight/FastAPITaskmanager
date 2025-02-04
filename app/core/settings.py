from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    SECRET_KEY: str = "Dgx2b9X1Vjvay/WmSXAJm720bbWgmLxRULv7xL2Q+RYkQmGdjZngMvcusgoUDsxtQAOu/ziy9kZ/mKTl3+QgRxDiAyeWmrgjZcH/u961isl2jkOKiPvPJcWetLusLM/S9I+2xH9AbX3EwS8daihBlxMAzwbMYlAy"  # Замените на случайную строку
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()