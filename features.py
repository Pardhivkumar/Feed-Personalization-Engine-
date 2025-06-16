def extract_features(post, user_profile):
    user_tags = user_profile["tags_followed"]
    buddies = user_profile["buddies"]
    active_hours = user_profile["active_hours"]
    author_branch_match = True  # You can simulate or skip this
    
    # Time match score
    post_hour = int(post["created_at"][11:13])
    time_match = 0.0
    for slot in active_hours:
        start, end = [int(x.split(":")[0]) for x in slot.split("-")]
        if start <= post_hour <= end:
            time_match = 1.0
            break

    return {
        "user_follows_tag": any(tag in user_tags for tag in post["tags"]),
        "is_buddy_post": post["author_id"] in buddies,
        "content_type": post["content_type"],
        "karma": post["karma"],
        "time_match_score": time_match,
        "author_branch_similarity": author_branch_match  # dummy value
    }
