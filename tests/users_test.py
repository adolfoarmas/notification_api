# import pytest
# from sqlalchemy import create_engine
# from src.database import Base, get_db
# from sqlalchemy.orm import scoped_session
# from sqlalchemy.orm import sessionmaker
# from src.database import Base
# from pydantic import ValidationError
# from src.users.models import User
# from fastapi.testclient import TestClient
# from src.main import app

# client = TestClient(app)

# @pytest.fixture(scope="function")
# def setup_db():
#     Base.metadata.create_all(bind=engine)  
#     yield  # Test runs here
#     Base.metadata.drop_all(bind=engine) 


# @pytest.fixture(scope="function")
# def client(setup_db):
#     def override_get_db():
#         db = TestingSessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()

#     app.dependency_overrides[get_db] = override_get_db
#     with TestClient(app) as c:
#         yield c

# """
# def test_create_user():
#     response = client.post("/api/notifications/users/", json={"name": "Manuel Rosales", "email": "mros@example.com", "phone": "98654523"})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Manuel Rosales"
#     assert data["email"] == "mros@example.com"
#     assert data["phone"] == "98654523"
# """

# def test_create_existing_email_phone_user(client):
#     response = client.post("/api/notifications/users/", json={"name": "Manuel Rosales", "email": "mros@example.com", "phone": "98654523"})
#     assert response.status_code == 409
#     assert response.json() == { "detail": "A user with the provided email or phone already exists." }

# def test_create_mo_email_no_phone_user(client):
#     response = client.post("/api/notifications/users/", json={"name": "Manuel Rosales", "email": "", "phone": ""})
#     assert response.status_code == 422
#     data = response.json()
#     assert data['detail'][0]['msg'] == "Value error, At least one of email or phone must be provided"

# def test_read_user(client):
#     user_id = 98 #use an existing client ID
#     response = client.get(f"/api/notifications/users/{str(user_id)}/")
#     assert response.status_code == 200

#     client.delete(f"/api/notifications/users/{str(user_id)}/")
#     assert response.status_code == 204

# def test_delete_unexistent_user(client):
#     response = client.delete("/api/notifications/users/9999") 
#     assert response.status_code == 404

# def test_user_not_found(client):
#     response = client.get("/api/notifications/users/9999") 
#     assert response.status_code == 404
#     assert response.json() == { "detail": "User not found" }