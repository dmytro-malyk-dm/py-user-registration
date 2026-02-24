from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY_ACCESS: str = Field(default="super-secret-key", env="SECRET_KEY_ACCESS")
    JWT_SIGNING_ALGORITHM: str = "HS256"
    AWS_ENDPOINT_URL: str
    SQS_QUEUE_URL: str
    S3_BUCKET_NAME: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
