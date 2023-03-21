import warnings
import os

import pytest
# from asgi_lifespan import LifespanManager

from fastapi import FastAPI
# from httpx import AsyncClient
from databases import Database
from async_asgi_testclient import TestClient



import alembic
from alembic.config import Config

from app.models.cleaning import CleaningCreate, CleaningInDB
from app.db.repositories.cleanings import CleaningsRepository


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope='session')
def apply_migrations():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    os.environ['TESTING'] = '1'
    config = Config('alembic.ini')
    
    alembic.command.upgrade(config, 'head')
    yield
    alembic.command.downgrade(config, 'base')


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application
    
    return get_application()

# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> TestClient:
    async with TestClient(app) as client:
        yield client


@pytest.fixture
async def test_cleaning(db: Database) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    new_cleaning = CleaningCreate(
        name="fake cleaning name",
        description="fake cleaning description",
        price=9.99,
        cleaning_type="spot_clean",
    )
    return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning)