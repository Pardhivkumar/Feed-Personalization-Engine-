# Feed Personalization Engine

A FastAPI microservice that ranks feed posts for students using ML and user interest features.

## Features
- ML-powered post scoring (RandomForest)
- Fully offline FastAPI backend
- Dockerized and testable locally
- Swagger API docs at /docs

## Setup

1. Clone repo
2. Install requirements:
   pip install -r requirements.txt
3. Train model:
   python train_model.py
4. Run locally:
   uvicorn main:app --reload --port 8000

## Run with Docker

docker build -t feed-personalizer .
docker run -p 8000:8000 feed-personalizer

## Test API

Visit http://localhost:8000/docs  
Use sample payloads to test the `/rank-feed` endpoint.

## Project Structure

- `main.py` — FastAPI app
- `ranker.py` — model loader + scoring
- `features.py` — feature extraction
- `train_model.py` — train RandomForest
- `model.pkl` — trained model
- `encoder.pkl` — for content_type

## Sample Input

{
  "user_id": "stu_4432",
  "posts": [...],
  "user_profile": { ... }
}

## Sample Output

{
  "user_id": "stu_4432",
  "ranked_posts": [...],
  "status": "ranked"
}
