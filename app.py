from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the weights for each criterion nhahahaha
WEIGHTS = {
    "total_jobs_ended": 0.2,
    "user_rating": 0.4,
    "total_money_earned": 0.3,
    "distance": 0.1
}

def safe_divide(numerator, denominator):
    """
    Safely divide two numbers, returning 0 if the denominator is zero.
    """
    return numerator / denominator if denominator != 0 else 0

def calculate_similarity(profile, target_profile):
    """
    Calculate similarity score between two profiles.
    """
    score = 0.0
    
    # Handle total_jobs_ended
    profile_jobs_ended = profile.get("total_jobs_ended", 0)
    target_jobs_ended = target_profile.get("total_jobs_ended", 0)
    score += WEIGHTS["total_jobs_ended"] * (1 - safe_divide(abs(profile_jobs_ended - target_jobs_ended), max(profile_jobs_ended, target_jobs_ended)))
    
    # Handle user_rating
    profile_rating = profile.get("user_rating", 0)
    target_rating = target_profile.get("user_rating", 0)
    score += WEIGHTS["user_rating"] * (1 - safe_divide(abs(profile_rating - target_rating), max(profile_rating, target_rating)))
    
    # Handle total_money_earned
    profile_money_earned = profile.get("total_money_earned", 0)
    target_money_earned = target_profile.get("total_money_earned", 0)
    score += WEIGHTS["total_money_earned"] * (1 - safe_divide(abs(profile_money_earned - target_money_earned), max(profile_money_earned, target_money_earned)))
    
    # Handle distance
    profile_distance = profile.get("distance", 0)
    target_distance = target_profile.get("distance", 0)
    score += WEIGHTS["distance"] * (1 - safe_divide(abs(profile_distance - target_distance), max(profile_distance, target_distance)))
    
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
    app.run( debug=True)
