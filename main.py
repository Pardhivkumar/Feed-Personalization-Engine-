from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from ranker import rank_posts
from features import extract_features

app = FastAPI()

# Pydantic Models
class Post(BaseModel):
    post_id: str
    author_id: str
    tags: List[str]
    content_type: str
    karma: int
    created_at: str

class UserProfile(BaseModel):
    branches_of_interest: List[str]
    tags_followed: List[str]
    buddies: List[str]
    active_hours: List[str]

class RankRequest(BaseModel):
    user_id: str
    posts: List[Post]
    user_profile: UserProfile

class RankedPost(BaseModel):
    post_id: str
    score: float

class RankResponse(BaseModel):
    user_id: str
    ranked_posts: List[RankedPost]
    status: str

@app.post("/rank-feed", response_model=RankResponse)
def rank_feed(request: RankRequest):
    try:
        ranked = rank_posts(request.user_profile.model_dump(), [p.model_dump() for p in request.posts], extract_features)
        return RankResponse(user_id=request.user_id, ranked_posts=ranked, status="ranked")
    except Exception as e:
        print(e)
        return RankResponse(user_id=request.user_id, ranked_posts=[], status="error")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"model_version": "1.0.0"}
