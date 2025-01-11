from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_STR: str = "/api"
    PROJECT_NAME: str = "BMW_CONNECTED_DRIVE"
    CAPCHA_TOKEN: str
    USERNAME: str
    PASSWORD: str
    VIN_NUMBER: str

settings = Settings()
