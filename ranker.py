import joblib
import pandas as pd

# Load model and encoder once
model = joblib.load("model.pkl")
encoder = joblib.load("encoder.pkl")

def rank_posts(user_profile, posts, extract_fn):
    feature_list = []
    post_ids = []

    for post in posts:
        features = extract_fn(post, user_profile)
        post_ids.append(post["post_id"])
        feature_list.append(features)

    df = pd.DataFrame(feature_list)

    # One-hot encode 'content_type'
    encoded = encoder.transform(df[["content_type"]])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(["content_type"]))
    
    df = df.drop("content_type", axis=1).reset_index(drop=True)
    final_features = pd.concat([df, encoded_df], axis=1)

    scores = model.predict(final_features)

    ranked = sorted(
        [{"post_id": pid, "score": float(score)} for pid, score in zip(post_ids, scores)],
        key=lambda x: x["score"],
        reverse=True
    )
    return ranked
