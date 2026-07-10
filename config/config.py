from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class NotFoundError(Exception):
    def __init__(self, resource: str, identifier: int | str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f'{resource} {identifier} not found')


class ConflictError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    app_name: str = Field(validation_alias='APP_NAME')
    database_url: str = Field(validation_alias='DATABASE_URL')
    static_url_prefix: str = Field(validation_alias='STATIC_URL_PREFIX')
    storage_url_prefix: str = Field(validation_alias='STORAGE_URL_PREFIX')
    templates_dir: Path = Field(validation_alias='TEMPLATES_DIR')
    static_dir: Path = Field(validation_alias='STATIC_DIR')
    storage_dir: Path = Field(validation_alias='STORAGE_DIR')


settings = Settings()
settings.templates_dir = BASE_DIR / settings.templates_dir
settings.static_dir = BASE_DIR / settings.static_dir
settings.storage_dir = BASE_DIR / settings.storage_dir
templates = Jinja2Templates(directory=str(settings.templates_dir))