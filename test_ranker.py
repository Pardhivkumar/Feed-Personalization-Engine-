from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_rank_basic():
    payload = {
        "user_id": "stu_1",
        "posts": [
            {
                "post_id": "p1",
                "author_id": "stu_2",
                "tags": ["coding"],
                "content_type": "text",
                "karma": 50,
                "created_at": "2024-07-01T10:00:00Z"
            }
        ],
        "user_profile": {
            "branches_of_interest": ["CSE"],
            "tags_followed": ["coding"],
            "buddies": ["stu_2"],
            "active_hours": ["08:00-12:00"]
        }
    }
    response = client.post("/rank-feed", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "ranked"
    assert result["ranked_posts"][0]["score"] > 0.7
