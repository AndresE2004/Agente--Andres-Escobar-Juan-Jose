from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "dev"
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    socrata_domain: str = "datos.gov.co"
    socrata_app_token: str | None = None

    database_url: str = "sqlite:///./app.db"


settings = Settings()

