from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db import engine, Base
from .routers import assistants, chats


@asynccontextmanager
async def lifespan(app: FastAPI):
    # -----  startup  -----
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield                                 # <- application is running


app = FastAPI(title="Mini-Assistant API", lifespan=lifespan)
app.include_router(assistants.router)
app.include_router(chats.router)
