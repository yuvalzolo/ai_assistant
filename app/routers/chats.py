from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from .. import models, schemas, services
from sqlalchemy.orm import selectinload
router = APIRouter(prefix="/chats", tags=["chats"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("", response_model=schemas.ChatOut, status_code=201)
async def start_chat(body: schemas.ChatCreate, db: AsyncSession = Depends(get_db)):
    assistant = await db.get(models.Assistant, body.assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")

    chat = models.Chat(assistant=assistant)
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat

@router.post("/{chat_id}/messages", response_model=schemas.MessageOut)
async def send_message(chat_id: int, body: schemas.MessageCreate, db: AsyncSession = Depends(get_db)):

    # ➋ use proper loader options
    chat = await db.get(
        models.Chat,
        chat_id,
        options=[
            selectinload(models.Chat.messages),
            selectinload(models.Chat.assistant),
        ],
    )
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # ➌ store user message
    user_msg = models.Message(chat=chat, role="user", content=body.content)
    db.add(user_msg)
    await db.flush()

    # ➍ build history
    history = [
        {"role": m.role, "content": m.content}
        for m in sorted(chat.messages + [user_msg], key=lambda m: m.created_at)
    ]

    assistant_reply = await services.run_chat(chat.assistant.system_prompt, history)

    # ➎ persist assistant response
    bot_msg = models.Message(chat=chat, role="assistant", content=assistant_reply)
    db.add(bot_msg)
    await db.commit()
    await db.refresh(bot_msg)
    return bot_msg

@router.get("/{chat_id}/messages", response_model=list[schemas.MessageOut])
async def list_messages(chat_id: int, db: AsyncSession = Depends(get_db)):
    chat = await db.get(models.Chat, chat_id, options=[selectinload(models.Chat.messages)])
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return sorted(chat.messages, key=lambda m: m.created_at)
