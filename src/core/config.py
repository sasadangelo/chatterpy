# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict
from pydantic_settings.sources import YamlConfigSettingsSource


class ProtocolName(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    WATSONX = "watsonx"


class ModelConfig(BaseModel):
    name: str
    parameters: dict[str, object] = {}


class ProtocolConfig(BaseModel):
    name: ProtocolName
    api_url: str
    model: ModelConfig
    space_id: str | None = None  # only watsonx


class MemoryType(str, Enum):
    BUFFER = "buffer"
    WINDOW = "window"
    SUMMARY = "summary"


class MemoryConfig(BaseModel):
    """Memory configuration settings."""

    chat_history: MemoryType = MemoryType.BUFFER
    chat_history_window: int | None = None  # only if chat_history==MemoryType.WINDOW


class DistanceFunction(str, Enum):
    COSINE = "Cosine"
    EUCLID = "Euclid"
    DOT = "Dot"


class RagConfig(BaseModel):
    """RAG (Retrieval Augmented Generation) configuration."""

    enabled: bool = False
    top_k_chunks: int = 10
    document_chunk_size: int = 100
    document_chunk_overlap: int = 0
    qdrant_path: str = "~/.qdrant"
    qdrant_collection: str = "mycollection"
    embedding_protocol: str = "ollama"
    embedding_model: str = "llama3.1:latest"
    embedding_vector_size: int = 4096
    embedding_distance_function: DistanceFunction = DistanceFunction.COSINE


class LogConfig(BaseSettings):
    """Logging configuration settings."""

    level: str = Field(default="INFO", description="Log level")
    console: bool = Field(default=True, description="Enable console logging")
    file: str | None = Field(default=None, description="Log file path")
    rotation: str = Field(default="10 MB", description="Log rotation size")
    retention: str = Field(default="7 days", description="Log retention period")
    compression: str = Field(default="zip", description="Log compression format")

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(extra="ignore")


class AppSettings(BaseSettings):
    protocol: ProtocolConfig
    system_message: str
    log: LogConfig
    datawave_log: LogConfig
    memory: MemoryConfig
    rag: RagConfig

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        yaml_file="config.yaml",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize settings sources: YAML file only."""
        return (
            YamlConfigSettingsSource(settings_cls),
            env_settings,
            init_settings,
        )


# Load settings at module import
chatterpy_config: AppSettings = AppSettings()  # type: ignore[call-arg]
