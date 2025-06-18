from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from .. import models, schemas
from sqlalchemy import select
router = APIRouter(prefix="/assistants", tags=["assistants"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("", response_model=schemas.AssistantOut,status_code=201)
async def create_assistant(body: schemas.AssistantCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(
        select(models.Assistant).where(models.Assistant.name == body.name)
    )
    if existing:
        raise HTTPException(status_code=400, detail="Name already exists")

    assistant = models.Assistant(**body.model_dump())
    db.add(assistant)
    await db.commit()
    await db.refresh(assistant)
    return assistant
