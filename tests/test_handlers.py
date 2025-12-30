import pytest
from src.database.core.db_setup import sync_session_factory
from src.database.core.db_models import Employee, Project, Task, Note
from src.routers import employee
import json


@pytest.mark.smoke
def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json() == {"message": "Hello world"}


# def test_create_employee(test_app, monkeypatch):
#     test_request_data = [
#         EmployeeBase(
#             first_name="Monkey",
#             last_name="Patched",
#             salary=12121,
#         )
#     ]
#     test_request_data2 = [
#         {
#             "first_name": "Monkey",
#             "last_name": "Patched",
#             "salary": 12121,
#         }
#     ]

#     async def mock_post(data):
#         return 1

#     monkeypatch.setattr(employee, "create_employees_handle", mock_post)

#     response = test_app.post("/employees/", content=json.dumps(test_request_data2))

#     print(response)


def test_read_employee(test_app, monkeypatch):
    # test_data = {"id": 1, "title": "something", "description": "something else"}

    # def mock_get():
    #     return test_data

    # monkeypatch.setattr(employee, "get_employees_handle", mock_get)

    response = test_app.get("/employees/")

    print(response)


# @pytest.mark.smoke
# def test_data():
#     with sync_session_factory() as session:
#         employee = session.get(Employee, 1)
#         assert isinstance(employee, dict)
#         assert employee["first_name"] == "James"
#         assert employee["last_name"] == "Wilson"
#         assert employee["salary"] == 85000
#         assert employee["is_working"] is True
