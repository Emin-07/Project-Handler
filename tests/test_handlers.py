import pytest
from src.database.connections.db_setup import sync_session_factory
from src.database.connections.db_models import Employee, Project, Task, Note
from main import employee
import json


@pytest.mark.smoke
def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json() == {"message": "Hello world"}


def test_create_employee(test_app, monkeypatch):
    test_request_data = [
        {
            "first_name": "Monkey",
            "last_name": "Patched",
            "salary": 12121,
        }
    ]

    async def mock_post(data):
        return 1

    monkeypatch.setattr(employee, "create_employees_handle", mock_post)

    response = test_app.post("/employees/", content=json.dumps(test_request_data))

    print(response.json())


# @pytest.mark.smoke
# def test_data():
#     with sync_session_factory() as session:
#         employee = session.get(Employee, 1)
#         assert isinstance(employee, dict)
#         assert employee["first_name"] == "James"
#         assert employee["last_name"] == "Wilson"
#         assert employee["salary"] == 85000
#         assert employee["is_working"] is True
