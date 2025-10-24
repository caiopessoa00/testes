from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from crm.constants import PIPELINE_STAGES
from crm.database import Base, engine, get_db
from crm.models import Lead
from crm.schemas import LeadCreate, LeadRead, StageUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRM de Leads",
    description="API simples para gerenciar leads manualmente ou via webhook.",
)


@app.get("/stages", summary="Listar etapas do funil")
def list_stages():
    return {"stages": PIPELINE_STAGES}


@app.post("/leads", response_model=LeadRead, status_code=201, summary="Criar lead manualmente")
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    db_lead = Lead(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        stage=lead.stage,
        source="manual",
    )

    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


@app.post(
    "/webhook/leads",
    response_model=LeadRead,
    status_code=201,
    summary="Receber lead via webhook",
)
def receive_lead_webhook(payload: LeadCreate, db: Session = Depends(get_db)):
    """Recebe leads de integrações externas."""
    db_lead = Lead(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        company=payload.company,
        stage=payload.stage,
        source="webhook",
    )

    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


@app.get("/leads", response_model=list[LeadRead], summary="Listar leads")
def list_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    return leads


@app.get("/leads/{lead_id}", response_model=LeadRead, summary="Detalhar lead")
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return lead


@app.patch(
    "/leads/{lead_id}/stage",
    response_model=LeadRead,
    summary="Atualizar etapa do funil",
)
def update_stage(lead_id: int, stage_update: StageUpdate, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")

    lead.stage = stage_update.stage
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
