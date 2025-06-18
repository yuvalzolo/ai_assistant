# tests/conftest.py

import sys
import pathlib
import pytest
from fastapi.testclient import TestClient
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.main import app
from app.db import engine, Base

@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    import asyncio

    async def setup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(setup())
    yield

# Provide a synchronous FastAPI test client
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
