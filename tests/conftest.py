import pytest
from src.database.queries.data_handler import add_data_into_db_sync
from src.database.connections.db_setup import sync_session_factory
import json
from main import app
from fastapi.testclient import TestClient

# @pytest.fixture(scope="session", autouse=True)
# def add_data_into_db():
#     with open("test_data.json") as f:
#         data = f.read()
#         data = json.loads(data)
#     print("loading data ...")
#     with sync_session_factory() as session:
#         add_data_into_db_sync(data=data, session=session)
#     print("adding data into test database...")


@pytest.fixture
def test_app():
    client = TestClient(app)
    yield client
