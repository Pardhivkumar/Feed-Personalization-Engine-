import random
import json
from datetime import datetime, timedelta

tags_pool = ['coding', 'events', 'startups', 'python', 'ai', 'design', 'sports']
content_types = ['text', 'image', 'poll', 'video']
branches = ['CSE', 'AI', 'ECE', 'EEE', 'MECH']
active_hour_slots = [["08:00-11:00"], ["21:00-23:00"], ["13:00-16:00"],["17:00-20:00"]]

def generate_random_post(i):
    return {
        "post_id": f"post_{1000 + i}",
        "author_id": f"stu_{random.randint(1000, 2000)}",
        "tags": random.sample(tags_pool, k=random.randint(1, 3)),
        "content_type": random.choice(content_types),
        "karma": random.randint(0, 100),
        "created_at": (datetime.utcnow() - timedelta(hours=random.randint(0, 48))).isoformat() + "Z"
    }

def generate_random_profile():
    return {
        "branches_of_interest": random.sample(branches, k=2),
        "tags_followed": random.sample(tags_pool, k=3),
        "buddies": [f"stu_{random.randint(1000, 2000)}" for _ in range(2)],
        "active_hours": random.choice(active_hour_slots)
    }

def calculate_time_match(post_time, active_hours):
    post_hour = int(post_time[11:13])  # extract hour from ISO timestamp
    for slot in active_hours:
        start_str, end_str = slot.split('-')
        start = int(start_str.split(':')[0])
        end = int(end_str.split(':')[0])
        if start <= post_hour <= end:
            return 1.0
    return round(random.uniform(0.2, 0.6), 2)


def compute_features(post, profile):
    return {
        "user_follows_tag": any(tag in profile["tags_followed"] for tag in post["tags"]),
        "is_buddy_post": post["author_id"] in profile["buddies"],
        "content_type": post["content_type"],
        "karma": post["karma"],
        "time_match_score": calculate_time_match(post["created_at"], profile["active_hours"]),
        "author_branch_similarity": random.choice([True, False])
    }

def assign_label(features):
    score = 0.3
    if features["user_follows_tag"]:
        score += 0.3
    if features["is_buddy_post"]:
        score += 0.2
    if features["karma"] > 50:
        score += 0.1
    score += features["time_match_score"] * 0.1
    return round(min(score, 1.0), 2)

# Generate data
dataset = []
for i in range(500):  # You can increase to 1000
    post = generate_random_post(i)
    profile = generate_random_profile()
    features = compute_features(post, profile)
    label = assign_label(features)
    dataset.append({"features": features, "label": label})

# Save to file
with open("training_data.json", "w") as f:
    json.dump(dataset, f, indent=2)
