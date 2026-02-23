from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY_ACCESS: str = Field(default="super-secret-key", env="SECRET_KEY_ACCESS")
    JWT_SIGNING_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
