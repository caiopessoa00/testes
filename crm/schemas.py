from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator

from .constants import DEFAULT_STAGE, PIPELINE_STAGES


def ensure_valid_stage(stage: str) -> str:
    if stage not in PIPELINE_STAGES:
        allowed = ", ".join(PIPELINE_STAGES)
        raise ValueError(f"Etapa inválida '{stage}'. Etapas permitidas: {allowed}")
    return stage


class LeadBase(BaseModel):
    name: str = Field(..., description="Nome completo do lead")
    email: Optional[EmailStr] = Field(None, description="Email de contato")
    phone: Optional[str] = Field(None, description="Telefone do lead")
    company: Optional[str] = Field(None, description="Empresa do lead")
    stage: str = Field(
        DEFAULT_STAGE,
        description="Etapa do funil em que o lead se encontra",
        examples=[DEFAULT_STAGE],
    )

    class Config:
        anystr_strip_whitespace = True

    @validator("stage")
    def validate_stage(cls, value: str) -> str:
        return ensure_valid_stage(value)


class LeadCreate(LeadBase):
    stage: str = Field(DEFAULT_STAGE, description="Etapa do funil")


class LeadRead(LeadBase):
    id: int
    stage: str
    source: str
    created_at: datetime

    class Config:
        orm_mode = True


class StageUpdate(BaseModel):
    stage: str = Field(..., description="Nova etapa do funil")

    @validator("stage")
    def validate_stage(cls, value: str) -> str:
        return ensure_valid_stage(value)
