from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Database Config
    db_username: str = Field(default="Mukesh")
    db_password: str = Field(default="Mukesh@95")
    db_hostname: str = Field(default="127.0.0.1")
    db_port: str = Field(default="3306")
    db_name: str = Field(default="ecom")

    # JWT Config
    secret_key: str = Field(default="your-secret")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)

    model_config = SettingsConfigDict(env_file=".env")  # ✅ for Pydantic v2


settings = Settings()
