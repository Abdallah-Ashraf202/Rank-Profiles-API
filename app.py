from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the weights for each criterion
WEIGHTS = {
    "total_jobs_ended": 0.2,
    "user_rating": 0.4,
    "total_money_earned": 0.3,
    "distance": 0.1
}

def calculate_similarity(profile, target_profile):
    """
    Calculate similarity score between two profiles.
    """
    score = 0.0
    score += WEIGHTS["total_jobs_ended"] * (1 - abs(profile["total_jobs_ended"] - target_profile["total_jobs_ended"]) / max(profile["total_jobs_ended"], target_profile["total_jobs_ended"]))
    score += WEIGHTS["user_rating"] * (1 - abs(profile["user_rating"] - target_profile["user_rating"]) / max(profile["user_rating"], target_profile["user_rating"]))
    score += WEIGHTS["total_money_earned"] * (1 - abs(profile["total_money_earned"] - target_profile["total_money_earned"]) / max(profile["total_money_earned"], target_profile["total_money_earned"]))
    score += WEIGHTS["distance"] * (1 - abs(profile["distance"] - target_profile["distance"]) / max(profile["distance"], target_profile["distance"]))
    return score

@app.route('/rank_profiles', methods=['POST'])
def rank_profiles():
    data = request.json
    target_profile = data["target_profile"]
    profiles = data["profiles"]
    
    # Calculate similarity scores for each profile
    ranked_profiles = []
    for profile in profiles:
        similarity_score = calculate_similarity(profile, target_profile)
        ranked_profiles.append((profile, similarity_score))
    
    # Sort profiles by similarity score in descending order
    ranked_profiles.sort(key=lambda x: x[1], reverse=True)
    
    # Return the sorted profiles
    ranked_profiles = [profile for profile, score in ranked_profiles]
    return jsonify(ranked_profiles)

if __name__ == '__main__':
    app.run(debug=True)