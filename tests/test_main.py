from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

#Channels

def test_create_channel():
    channels = ["SMS", "Email", "Push"]
    for channel in channels:
        response = client.post("/api/notifications/channels/", json={"type": channel})
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == channel

#Categories
def test_create_category():
    categories = ["Sports", "Finance", "Films"]
    for category in categories:
        response = client.post("/api/notifications/categories/", json={"name": category})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == category

#Users
def test_create_user():
    response = client.post("/api/notifications/users/", 
                json={"name": "Manuel Rosales", 
                    "email": "mros@example.com", 
                    "phone": "98654523", 
                    "subscribed_categories": [1],
                    "subscribed_channels": [1,2]
                })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Manuel Rosales"
    assert data["email"] == "mros@example.com"
    assert data["phone"] == "98654523"
    assert data["subscribed_categories"] == [1]
    assert data["subscribed_channels"] == [1,2]


    response = client.post("/api/notifications/users/", 
                json={"name": "Manuela Rosales", 
                    "email": "maros@example.com", 
                    "phone": "98654522", 
                    "subscribed_categories": [1, 3],
                    "subscribed_channels": [3]
                })

    response = client.post("/api/notifications/users/", 
            json={"name": "Manuela Rosal", 
                "email": "marosal@example.com", 
                "phone": "98654521", 
                "subscribed_categories": [2, 3],
                "subscribed_channels": [1]
            })

def test_create_existing_email_phone_user():
    response = client.post("/api/notifications/users/", json={"name": "Manuel Rosales", "email": "mros@example.com", "phone": "98654523"})
    assert response.status_code == 409
    assert response.json() == { "detail": "A user with the provided email or phone already exists." }

def test_create_no_email_no_phone_user():
    response = client.post("/api/notifications/users/", json={"name": "Manuel Rosales", "email": "", "phone": ""})
    assert response.status_code == 422
    data = response.json()
    assert data['detail'][0]['msg'] == "Value error, At least one of email or phone must be provided"

def test_read_user():
    user_id = 1 #use an existing client ID
    response = client.get(f"/api/notifications/users/{str(user_id)}/")
    assert response.status_code == 200

    client.delete(f"/api/notifications/users/{str(user_id)}/")
    assert response.status_code == 200

def test_delete_unexistent_user():
    response = client.delete("/api/notifications/users/9999") 
    assert response.status_code == 404

def test_user_not_found():
    response = client.get("/api/notifications/users/9999") 
    assert response.status_code == 404
    assert response.json() == { "detail": "User not found" }

#Notifications
def test_create_notification_success():
    response = client.post("/api/notifications/send/", json={"category": 2, "message": "Test message"})
    assert response.status_code == 200
    assert response.json() == [{"user_id": 3, "channel": "SMS", "status": "ok"}]

def test_create_notification_invalid_category():
    category = 5
    response = client.post("/api/notifications/send/", json={"category": category, "message": "Test message"})
    assert response.status_code == 404
    assert response.json() == {"detail": f"Users to notify not found, ensure the category id {category} is correct"}
