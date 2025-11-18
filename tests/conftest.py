# import pytest
# import pytest_asyncio
# from src.database.queries.data_handler import reset_data
# from src.database.connections.db_setup import async_session_factory
# import json
# from main import app
# from fastapi.testclient import TestClient


# # @pytest_asyncio.fixture(scope="session")
# # async def setup_db():
# #     async with async_session_factory() as session:
# #         await reset_data(session)


# @pytest.fixture
# def test_app():
#     client = TestClient(app)
#     yield client
