import os
import sys
app_dir = os.path.join(os.path.dirname(__file__),"..")
sys.path.append(app_dir)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session,sessionmaker
from database import get_db
from main import app
from fastapi.testclient import TestClient
from models import Base,Item
from datetime import date
from schemas import DecodedToken
from cruds.auth import get_current_user


@pytest.fixture()
def session_fixture():
    engine = create_engine(
        url = "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
    db = SessionLocal()

    try:
        today = date.today()
        task1 = Item(title="kaimono1",content="milk",due_date=today,completed=False,user_id="1")
        task2 = Item(title="kaimono2",content="pasta",due_date=date(2025,10,30),completed=False,user_id="1")
        db.add(task1)
        db.add(task2)
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture()
def user_fixture():
    return DecodedToken(username='user1',user_id=1)

@pytest.fixture()
def client_fixture(session_fixture: Session,user_fixture :DecodedToken):
    def override_get_db():
        return session_fixture
    
    def override_get_current_user():
        return user_fixture

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
